import json
import boto3
import datetime
import logging
import csv
import os
import json
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from send_email import mail_main

# Set up logging
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

# Initialize AWS clients
# ec2_client = boto3.client('ec2')
# backup_client = boto3.client('backup')
s3_client = boto3.client("s3")

# Retrieve environment variables
bucket_name = os.environ.get("bucket_name", "")
file_name = os.environ.get("file_name", "")
email_subject = os.environ.get("email_subject", "")
recipient = os.environ.get("recipient", "")
report_title = os.environ.get("report_title", "")
temp_file_path = os.environ.get("temp_file_path", "")
aws_region = os.environ.get("aws_region", "")
aws_account_id = os.environ.get("aws_account_id", "")

# Get today's date
report_date = datetime.datetime.today().strftime("%Y-%m-%d")


def get_backup_details(instance_id, account_id, backup_client):
    """
    Retrieve backup details for a specific EC2 instance.

    Parameters:
        instance_id (str): The ID of the EC2 instance.

    Returns:
        list: Backup details for the instance.
    """
    try:
        response = backup_client.list_recovery_points_by_resource(
            ResourceArn=f"arn:aws:ec2:ap-south-1:{account_id}:instance/{instance_id}"
        )
        return response.get("RecoveryPoints", [])
    except Exception as e:
        LOGGER.error(f"Error retrieving backup details for instance {instance_id}: {e}")
        return []


def validate_sheet(raw_data, master_data):
    """
    Validates the raw_data DataFrame against the master_data DataFrame by checking
    which rows from raw_data are present in master_data (based on 'InstanceName').

    For matched/present rows, adds a 'BackupCountMatch' column indicating whether the
    'BackupCount' values in raw_data and master_data match.

    Parameters:
        raw_data (pd.DataFrame): The raw data DataFrame to be validated.
        master_data (pd.DataFrame): The master reference DataFrame.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]:
            - matched_df: rows from raw_data that matched master_data, with an additional 'BackupCountMatch' column.
            - missing_df: rows from raw_data that were not found in master_data.
    """
    merged_sheet = pd.merge(
        left=raw_data, right=master_data, how="left", on=["InstanceName"]
    )

    matched_rows = merged_sheet.loc[merged_sheet["InstanceID_y"].notna()]
    missing_rows = merged_sheet.loc[merged_sheet["InstanceID_y"].isna()]

    matched_df = raw_data.loc[matched_rows.index]
    missing_df = raw_data.loc[missing_rows.index]

    matched_df["BackupCountMatch"] = (
        matched_rows["BackupCount_x"] == matched_rows["BackupCount_y"]
    )

    return matched_df, missing_df


def swap_column_values(df, col1, col2):
    """
    Swaps the values of two columns in a DataFrame.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the columns.
        col1 (str): The name of the first column to swap.
        col2 (str): The name of the second column to swap.

    Returns:
        pd.DataFrame: The DataFrame with values of col1 and col2 swapped.
    """
    df[col1], df[col2] = df[col2].copy(), df[col1].copy()
    return df


def lambda_handler(event, context):
    try:
        role_name = os.environ.get("role_name", "")
        account_ids = os.environ.get("account_ids", "")
        split_ids = account_ids.split(",")
        account_id_list = [x.strip() for x in split_ids]
        findings_dict = {}
        backup_data_dict = {}
        backup_filter = os.environ.get("backup_filter", "")
        backup_filter_dict = json.loads(backup_filter)
        for account_id in account_id_list:
            LOGGER.info("Start getting non-complaint details")
            non_compliant_rules = []
            sts_client = boto3.client("sts")
            assumed_role = sts_client.assume_role(
                RoleArn=f"arn:aws:iam::{account_id}:role/{role_name}",
                RoleSessionName="crossAccountSession",
            )
            # client = boto3.client('config')
            credentials = assumed_role["Credentials"]
            session = boto3.Session(
                aws_access_key_id=credentials["AccessKeyId"],
                aws_secret_access_key=credentials["SecretAccessKey"],
                aws_session_token=credentials["SessionToken"],
            )

            # Get instances with Backup_Retention tag
            # filters = [
            #     {'Name': 'tag:Backup_Retention', 'Values': ["7-Days", "5-Days", "3-Days", "Monthly"]},
            # ]

            filters = [backup_filter_dict[account_id]]

            ec2_client = session.client("ec2")
            backup_client = session.client("backup")
            response = ec2_client.describe_instances(Filters=filters)
            instances_to_reports = [
                instance
                for reservation in response["Reservations"]
                for instance in reservation["Instances"]
            ]

            # Prepare backup details for each instance
            backup_data = []
            for instance in instances_to_reports:
                instance_id = instance["InstanceId"]
                instance_name = next(
                    (tag["Value"] for tag in instance["Tags"] if tag["Key"] == "Name"),
                    "Unnamed",
                )

                backup_details = get_backup_details(
                    instance_id, account_id, backup_client
                )
                backup_count = len(backup_details)

                # Serialize recovery_points to string
                recovery_points = json.dumps(backup_details, default=str)

                backup_data.append(
                    {
                        "InstanceID": instance_id,
                        "InstanceName": instance_name,
                        "BackupCount": backup_count,
                        "RecoveryPoints": recovery_points,
                        "ValidationDate": report_date,
                    }
                )
            backup_data_dict[account_id] = backup_data

        # Generate CSV file
        str_time_stamp = datetime.datetime.now().strftime("%Y%m%d")
        local_file_name = f"{file_name}_{str_time_stamp}.xlsx"
        local_file_path = f"{temp_file_path}{local_file_name}"
        headers = ["InstanceID", "InstanceName", "BackupCount", "RecoveryPoints"]
        # with open(local_file_path, "w", newline='') as csvfile:
        #     writer = csv.DictWriter(csvfile, fieldnames=headers)
        #     writer.writeheader()
        #     writer.writerows(backup_data)

        # Loading master data file
        master_data_file = "path/to/master/file"
        master_data = pd.read_excel(master_data_file, sheet_name=None)

        output_sheets = {}
        for accountid, rows_list in backup_data_dict.items():
            try:
                master_df = master_data[accountid]
            except KeyError as e:
                LOGGER.error(f"{accountid} absent in master sheet: {e}")

            raw_df = pd.DataFrame(rows_list)

            # Special handling for Azure sheet:
            # Azure environment uses InstanceID as unique identifier instead of InstanceName
            # Therefore, swap values between InstanceID and InstanceName columns for consistency
            if accountid == "Azure":
                raw_df = swap_column_values(raw_df, "InstanceID", "InstanceName")
                master_df = swap_column_values(master_df, "InstanceID", "InstanceName")

            matched_df, missing_df = validate_sheet(raw_df, master_df)

            # Swap columns back for Azure to restore original schema before exporting
            if accountid == "Azure":
                matched_df = swap_column_values(
                    matched_df, "InstanceID", "InstanceName"
                )
                missing_df = swap_column_values(
                    missing_df, "InstanceID", "InstanceName"
                )

            output_sheets[accountid] = matched_df
            output_sheets[f"{accountid}_Missing"] = missing_df

        # Write all processed sheets to a single Excel
        with pd.ExcelWriter(local_file_path) as excel_writer:
            for sheet_name, df in output_sheets.items():
                df.to_excel(excel_writer, sheet_name=sheet_name, index=False)

        # Upload CSV file to S3
        s3_file_path = f"ec2-backup-reports/{str_time_stamp}/{local_file_name}"
        s3_client.upload_file(local_file_path, bucket_name, s3_file_path)

        # Send email notification
        email_subject_with_date = f"{email_subject} {report_date}"
        mail_main(email_subject_with_date, local_file_name, local_file_path)

        LOGGER.info("Backup report generated and sent successfully.")
    except Exception as e:
        LOGGER.error(f"Exception occurred: {e}", exc_info=True)
