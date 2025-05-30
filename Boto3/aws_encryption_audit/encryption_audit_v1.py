import os
import logging
import boto3
import pandas as pd

from send_email import mail_main

LOGGER = logging.getLogger("encryption")
LOGGER.setLevel(logging.INFO)

s3_client = boto3.client("s3", region_name="ap-south-1")

rds_client = boto3.client("rds", region_name="ap-south-1")
rds_regions = ["ap-south-1"]

ec2_client = boto3.client("ec2", region_name="ap-south-1")
ebs_regions = ["ap-south-1"]


# Function to get S3 encryption status and key
def get_s3_encryption(bucket_name):
    try:
        encryption_config = s3_client.get_bucket_encryption(Bucket=bucket_name)
        if "ServerSideEncryptionConfiguration" in encryption_config:
            sse_algorithm = encryption_config["ServerSideEncryptionConfiguration"][
                "Rules"
            ][0]["ApplyServerSideEncryptionByDefault"]["SSEAlgorithm"]
            if sse_algorithm == "aws:kms":
                kms_key_id = encryption_config["ServerSideEncryptionConfiguration"][
                    "Rules"
                ][0]["ApplyServerSideEncryptionByDefault"]["KMSMasterKeyID"]
                return "Encrypted", kms_key_id
            else:
                return "Encrypted", sse_algorithm  # Non-KMS encryption
        return "Not Encrypted", "N/A"
    except s3_client.exceptions.ClientError as e:
        if (
            e.response["Error"]["Code"]
            == "ServerSideEncryptionConfigurationNotFoundError"
        ):
            return "Not Encrypted", "N/A"
        else:
            raise


# Function to get RDS encryption status
def get_rds_encryption(instance_id, region):
    try:
        response = rds_client.describe_db_instances(DBInstanceIdentifier=instance_id)
        return (
            "Enabled" if response["DBInstances"][0]["StorageEncrypted"] else "Disabled"
        )
    except rds_client.exceptions.DBInstanceNotFoundFault:
        return "Disabled"


# Function to get EBS encryption status
def get_ebs_encryption(volume_id, region):
    try:
        response = ec2_client.describe_volumes(VolumeIds=[volume_id])
        return "Enabled" if response["Volumes"][0]["Encrypted"] else "Disabled"
    except ec2_client.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "InvalidVolume.NotFound":
            return "Disabled"
        else:
            raise


# Function to retrieve AWS resources and write to DataFrame
def retrieve_and_write():
    
    # S3
    LOGGER.info("Start getting s3 encryption details")
    s3_data = []
    s3_buckets = s3_client.list_buckets()["Buckets"]
    for bucket in s3_buckets:
        bucket_name = bucket["Name"]
        project = ""
        try:
            tags = s3_client.get_bucket_tagging(Bucket=bucket_name)
            for tag in tags["TagSet"]:
                if tag["Key"] == "Project":
                    project = tag["Value"]
                    break
        except Exception as error:
            LOGGER.error(
                f"tag is not available for bucket {bucket} and exception is {error}",
                exc_info=True,
            )
        encryption_status, encryption_key = "Failed", "Failed"
        try:
            encryption_status, encryption_key = get_s3_encryption(bucket_name)
        except Exception as en_error:
            LOGGER.error(
                f"getting encryption details of {bucket} is failed and exception is {en_error}",
                exc_info=True,
            )
        s3_data.append([bucket_name, encryption_status, encryption_key, project])
    LOGGER.info("End getting s3 encryption details")

    # RDS
    LOGGER.info("Start getting RDS encryption details")
    rds_data = []
    for region in rds_regions:
        rds_client = boto3.client("rds", region_name=region)
        instances = rds_client.describe_db_instances()["DBInstances"]
        for instance in instances:
            instance_id = instance["DBInstanceIdentifier"]
            engine = instance["Engine"]
            dbclass = instance["DBInstanceClass"]
            project = ""
            tags = rds_client.list_tags_for_resource(
                ResourceName=instance["DBInstanceArn"]
            )["TagList"]
            for tag in tags:
                if tag["Key"] == "Project":
                    project = tag["Value"]
                    break
            encryption = get_rds_encryption(instance_id, region)
            rds_data.append([instance_id, engine, dbclass, region, encryption, project])
    LOGGER.info("End getting RDS encryption details")

    # EBS
    LOGGER.info("Start getting EBS encryption details")
    ebs_data = []
    for region in ebs_regions:
        ec2_client = boto3.client("ec2", region_name=region)
        volumes = ec2_client.describe_volumes()["Volumes"]
        for volume in volumes:
            volume_id = volume["VolumeId"]
            state = volume["State"]
            attachment = (
                volume["Attachments"][0]["InstanceId"]
                if volume["Attachments"]
                else "Not attached"
            )
            project = ""
            tags = ec2_client.describe_tags(
                Filters=[{"Name": "resource-id", "Values": [volume_id]}]
            )["Tags"]
            for tag in tags:
                if tag["Key"] == "Project":
                    project = tag["Value"]
                    break
            encryption = get_ebs_encryption(volume_id, region)
            ebs_data.append([volume_id, state, attachment, region, encryption, project])
    LOGGER.info("End getting EBS encryption details")

    # Create DataFrames
    LOGGER.info("Start creating s3 df object")
    s3_df = pd.DataFrame(
        s3_data,
        columns=["S3 Bucket Name", "Encryption Status", "Encryption Key", "Project"],
    )
    LOGGER.info("End creating s3 df object")
    LOGGER.info("Start creating RDS df object")
    rds_df = pd.DataFrame(
        rds_data,
        columns=[
            "RDS Instance Id",
            "Type",
            "Class",
            "Region",
            "Storage Encryption",
            "Project",
        ],
    )
    LOGGER.info("End creating RDS df object")
    LOGGER.info("Start creating EBS df object")
    ebs_df = pd.DataFrame(
        ebs_data,
        columns=[
            "Volume Id",
            "State",
            "Attachment Instance Id",
            "Region",
            "Encryption",
            "Project",
        ],
    )
    LOGGER.info("End creating EBS df object")
    return s3_df, rds_df, ebs_df


def lambda_handler(event, contex):
    """ """
    file_name = os.environ.get("filename", "")
    if not file_name:
        print("filename is not exist. Please check env variable")
        return
    file_dir = os.environ.get("file_dir", "")
    if not file_dir:
        print("file directory is not exist. Please check env variable")
        return
    file_path = f"{file_dir}{file_name}"
    # Initialize AWS clients

    # Retrieve data and write to DataFrames
    s3_df, rds_df, ebs_df = retrieve_and_write()

    LOGGER.info(f"Start writing excel file and file name_is {file_path}")
    # Convert DataFrames to XLSX and merge
    with pd.ExcelWriter(file_path) as writer:
        s3_df.to_excel(writer, sheet_name="S3", index=False)
        rds_df.to_excel(writer, sheet_name="RDS", index=False)
        ebs_df.to_excel(writer, sheet_name="EBS", index=False)
    LOGGER.info(f"End writing excel file.")

    LOGGER.info("Start Sending Email")
    email_top_headers = "Hi Team,<br><br>"
    email_headers = "<br><br><br>Regards,<br>PwC Support Team"
    email_message = (
        "We have generated the encryption report."
        "<br>Please check attached document.<br><br>"
    )

    email_message = f"{email_top_headers}{email_message}{email_headers}"
    mail_main(email_message, file_name, file_path)
    LOGGER.info("End Sending Email")
