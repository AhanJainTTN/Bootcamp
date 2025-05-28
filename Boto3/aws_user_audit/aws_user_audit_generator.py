import os
import time
import logging
from datetime import datetime

import boto3
import pandas as pd
from botocore.exceptions import BotoCoreError, ClientError

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# AWS clients
ec2 = boto3.client("ec2")
ssm = boto3.client("ssm")


def get_instance_details():
    """
    Retrieves EC2 instance IDs, names, and platform details.
    """
    try:
        response = ec2.describe_instances()
        instance_details = []

        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                instance_id = instance["InstanceId"]
                platform = instance.get("PlatformDetails", "Linux/UNIX")

                # Extract Name tag
                name = next(
                    (
                        tag["Value"]
                        for tag in instance.get("Tags", [])
                        if tag["Key"] == "Name"
                    ),
                    "",
                )
                instance_details.append(
                    {"InstanceID": instance_id, "Name": name, "Platform": platform}
                )

        return instance_details

    except (BotoCoreError, ClientError) as e:
        logging.error(f"Failed to describe EC2 instances: {e}")
        return []


def run_ssm_command(instance_ids, document_name):
    """
    Sends SSM command to the given instance IDs using the specified document.
    """
    try:
        response = ssm.send_command(
            InstanceIds=instance_ids,
            DocumentName=document_name,
            TimeoutSeconds=180,
        )
        command_id = response["Command"]["CommandId"]
        logging.info(f"SSM command sent. Command ID: {command_id}")
        return command_id

    except (BotoCoreError, ClientError) as e:
        logging.error(f"Failed to send SSM command: {e}")
        return None


def get_command_output(command_id, instance_id):
    """
    Fetches the output of an SSM command for a specific instance.
    """
    try:
        response = ssm.get_command_invocation(
            CommandId=command_id, InstanceId=instance_id
        )
        return response.get("StandardOutputContent", "").strip()

    except ssm.exceptions.InvocationDoesNotExist as e:
        logging.warning(f"Output not yet available for {instance_id}: {e}")
        raise
    except (BotoCoreError, ClientError) as e:
        logging.error(f"Error fetching output for {instance_id}: {e}")
        return "Error retrieving output"


def fetch_user_data(document_name, max_wait=180, poll_interval=3):
    """
    Orchestrates the user info retrieval across all instances.
    """
    instance_details = get_instance_details()
    if not instance_details:
        logging.error("No instance details found. Exiting.")
        return []

    instance_ids = [inst["InstanceID"] for inst in instance_details]
    command_id = run_ssm_command(instance_ids, document_name)
    if not command_id:
        return []

    waited = 0
    while waited < max_wait:
        time.sleep(poll_interval)
        waited += poll_interval

        try:
            for instance in instance_details:
                instance["Users"] = get_command_output(
                    command_id, instance["InstanceID"]
                )
            return instance_details  # Success, return early

        except ssm.exceptions.InvocationDoesNotExist:
            logging.info("Waiting for command output to become available...")

    logging.error("Timed out waiting for SSM command outputs.")
    return instance_details


def generate_excel_report(data, output_path):
    """
    Writes the final report to an Excel file.
    """
    try:
        df = pd.DataFrame(data)
        with pd.ExcelWriter(output_path) as writer:
            df.to_excel(writer, sheet_name="AWS User Audit", index=False)
        logging.info(f"Report saved to: {output_path}")
    except Exception as e:
        logging.error(f"Failed to write Excel report: {e}")


def main():
    document_name = "GetUserInfoShell"
    audit_data = fetch_user_data(document_name)

    if not audit_data:
        logging.error("No audit data retrieved. Exiting.")
        return

    report_date = datetime.today().strftime("%Y_%m_%d")
    # output_path = os.path.join(
    #     os.path.dirname(__file__), "files", f"AWS_User_Audit_{report_date}.xlsx"
    # )
    output_path = os.path.expanduser(
        f"~/aws_user_audit/AWS_User_Audit_{report_date}.xlsx"
    )

    generate_excel_report(audit_data, output_path)


if __name__ == "__main__":
    main()
