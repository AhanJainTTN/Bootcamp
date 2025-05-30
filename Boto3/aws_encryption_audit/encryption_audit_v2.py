import os
import logging
import boto3
import pandas as pd
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# AWS Clients
s3_client = boto3.client("s3")
rds_client = boto3.client("rds")
ec2_client = boto3.client("ec2")


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
                return "Encrypted", sse_algorithm
        return "Not Encrypted", "N/A"
    except s3_client.exceptions.ClientError as e:
        if (
            e.response["Error"]["Code"]
            == "ServerSideEncryptionConfigurationNotFoundError"
        ):
            return "Not Encrypted", "N/A"
        else:
            raise


def get_rds_encryption(instance_id):
    try:
        response = rds_client.describe_db_instances(DBInstanceIdentifier=instance_id)
        return (
            "Enabled" if response["DBInstances"][0]["StorageEncrypted"] else "Disabled"
        )
    except rds_client.exceptions.DBInstanceNotFoundFault:
        return "Disabled"


def get_ebs_encryption(volume_id):
    try:
        response = ec2_client.describe_volumes(VolumeIds=[volume_id])
        return "Enabled" if response["Volumes"][0]["Encrypted"] else "Disabled"
    except ec2_client.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "InvalidVolume.NotFound":
            return "Disabled"
        else:
            raise


def retrieve_and_write():
    s3_data, rds_data, ebs_data = [], [], []

    # S3
    logging.info("Collecting S3 encryption info...")

    s3_buckets = s3_client.list_buckets()["Buckets"]
    for bucket in s3_buckets:
        name = bucket["Name"]
        project = ""
        try:
            tags = s3_client.get_bucket_tagging(Bucket=name)
            project = next(
                (tag["Value"] for tag in tags["TagSet"] if tag["Key"] == "Project"), ""
            )
        except Exception:
            logging.warning(f"No tags for bucket {name}")
        try:
            enc_status, enc_key = get_s3_encryption(name)
        except Exception as e:
            logging.error(f"Error checking S3 encryption for {name}: {e}")
            enc_status, enc_key = "Failed", "Failed"
        s3_data.append([name, enc_status, enc_key, project])

    # RDS
    logging.info("Collecting RDS encryption info...")
    instances = rds_client.describe_db_instances()["DBInstances"]
    for instance in instances:
        inst_id = instance["DBInstanceIdentifier"]
        engine = instance["Engine"]
        db_class = instance["DBInstanceClass"]
        project = ""
        tags = rds_client.list_tags_for_resource(
            ResourceName=instance["DBInstanceArn"]
        )["TagList"]
        for tag in tags:
            if tag["Key"] == "Project":
                project = tag["Value"]
                break
        encryption = get_rds_encryption(inst_id)
        rds_data.append([inst_id, engine, db_class, encryption, project])

    # EBS
    logging.info("Collecting EBS encryption info...")
    volumes = ec2_client.describe_volumes()["Volumes"]
    for vol in volumes:
        vol_id = vol["VolumeId"]
        state = vol["State"]
        attach = (
            vol["Attachments"][0]["InstanceId"]
            if vol["Attachments"]
            else "Not attached"
        )
        project = ""
        tags = ec2_client.describe_tags(
            Filters=[{"Name": "resource-id", "Values": [vol_id]}]
        )["Tags"]
        for tag in tags:
            if tag["Key"] == "Project":
                project = tag["Value"]
                break
        encryption = get_ebs_encryption(vol_id)
        ebs_data.append([vol_id, state, attach, encryption, project])

    # Create DataFrames
    s3_df = pd.DataFrame(
        s3_data,
        columns=["S3 Bucket Name", "Encryption Status", "Encryption Key", "Project"],
    )
    rds_df = pd.DataFrame(
        rds_data,
        columns=[
            "RDS Instance Id",
            "Type",
            "Class",
            "Storage Encryption",
            "Project",
        ],
    )
    ebs_df = pd.DataFrame(
        ebs_data,
        columns=[
            "Volume Id",
            "State",
            "Attachment Instance Id",
            "Encryption",
            "Project",
        ],
    )
    
    return s3_df, rds_df, ebs_df


def main():
    s3_df, rds_df, ebs_df = retrieve_and_write()

    report_date = datetime.today().strftime("%Y_%m_%d")
    output_path = os.path.expanduser(
        f"~/aws_encryption_audit/AWS_Encryption_Audit_{report_date}.xlsx"
    )

    with pd.ExcelWriter(output_path) as writer:
        s3_df.to_excel(writer, sheet_name="S3", index=False)
        rds_df.to_excel(writer, sheet_name="RDS", index=False)
        ebs_df.to_excel(writer, sheet_name="EBS", index=False)

    logging.info(f"Report saved to: {output_path}")


if __name__ == "__main__":
    main()
