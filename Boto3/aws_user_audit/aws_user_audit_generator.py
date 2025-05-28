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

# Config
DOCUMENT = "AWS-RunShellScript"
COMMANDS = {
    "Linux/UNIX": ["getent passwd | awk -F: '/\/bin\/bash|\/bin\/false/ {print $1}'"],
    "Windows": ["Get-LocalUser | Select-Object -ExpandProperty Name"],
}
PLATFORMS = ["Linux", "Windows"]
BATCH_SIZE = 50


def get_instance_details():
    """
    Retrieves EC2 instance IDs, names, state and platform details.
    """
    try:
        paginator = ec2.get_paginator("describe_instances")
        pages = paginator.paginate()

        instance_details = []
        for page in pages:
            for reservation in page["Reservations"]:
                for instance in reservation["Instances"]:
                    instance_id = instance["InstanceId"]
                    platform = instance.get("PlatformDetails", "Other")
                    state = instance["State"]["Name"]

                    # Extract Name tag
                    name = ""
                    for tag in instance.get("Tags", []):
                        if tag["Key"] == "Name":
                            name = tag["Value"]
                            break

                    instance_details.append(
                        {
                            "InstanceID": instance_id,
                            "Name": name,
                            "Platform": platform,
                            "State": state,
                            "Users": "-",
                        }
                    )

        return instance_details

    except (BotoCoreError, ClientError) as e:
        logging.error(f"Failed to describe EC2 instances: {e}")
        return []


def run_ssm_command(instance_ids, document_name, commands, platform):
    """
    Sends SSM command to the given instance IDs using the specified document.
    """
    parameters = (
        {"commands": commands["Linux/UNIX"]}
        if platform == "Linux"
        else {"commands": commands[platform]}
    )

    try:
        response = ssm.send_command(
            InstanceIds=instance_ids,
            DocumentName=document_name,
            Parameters=parameters,
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
        return response.get("StandardOutputContent", "")

    except ssm.exceptions.InvocationDoesNotExist as e:
        logging.warning(f"Output not yet available for {instance_id}: {e}")
        raise
    except (BotoCoreError, ClientError) as e:
        logging.error(f"Error fetching output for {instance_id}: {e}")
        return None


def get_ssm_managed_instance_ids(platform):
    """
    Returns a list of instance IDs for a specified platform which have Online PingStatus
    and registered with SSM.
    """
    paginator = ssm.get_paginator("describe_instance_information")
    pages = paginator.paginate(Filters=[{"Key": "PlatformTypes", "Values": [platform]}])

    managed_ids = []
    for page in pages:
        for info in page["InstanceInformationList"]:
            instance_id = info.get("InstanceId")
            ping_status = info.get("PingStatus")

            if instance_id and ping_status and ping_status == "Online":
                managed_ids.append(info["InstanceId"])
            else:
                logging.error(
                    f"Instance is registered under SSM but not reachable: {instance_id}"
                )

    return managed_ids


def process_batch(command_id, managed_ids, max_wait, poll_interval):
    completed_instances = set()
    command_outputs = {}

    wait_time = 0
    while wait_time < max_wait:

        # wait for some time
        time.sleep(poll_interval)
        wait_time += poll_interval

        for instance_id in managed_ids:
            if instance_id in completed_instances:
                continue

            try:
                logging.info(f"Fetching command output for instance {instance_id}")
                command_output = get_command_output(command_id, instance_id)
                command_outputs[instance_id] = command_output
                completed_instances.add(instance_id)
            except ssm.exceptions.InvocationDoesNotExist:
                logging.info(f"Command output not ready for {instance_id}")

        if len(completed_instances) == len(managed_ids):
            logging.info(
                f"All command outputs retrieved. Processed {len(command_outputs)} out of {len(managed_ids)} for the current batch."
            )
            return command_outputs

    logging.warning(
        f"Timed out waiting for SSM command outputs. Processed {len(command_outputs)} out of {len(managed_ids)}"
    )

    return command_outputs


def batch_process(items, batch_size):
    for i in range(0, len(items), batch_size):
        yield items[i : i + batch_size]


def fetch_user_data(
    document_name,
    commands,
    platform,
    batch_size=BATCH_SIZE,  # size of the batch to be processed at once
    max_wait=20,  # max wait time to process a batch
    poll_interval=2,  # time between retries for a single batch
):
    """
    Starts the user info retrieval across all instances for a particular platform.
    """
    logging.info(f"Started retrieval for {platform} instances")

    # get all ids which are online and registered
    managed_ids = get_ssm_managed_instance_ids(platform=platform)

    # get command id for output retrieval
    command_id = run_ssm_command(
        managed_ids, document_name, commands, platform=platform
    )

    if not command_id:
        return []

    all_command_outputs = {}
    for batch in batch_process(managed_ids, batch_size):
        command_ouputs = process_batch(
            command_id, batch, max_wait=max_wait, poll_interval=poll_interval
        )
        all_command_outputs.update(command_ouputs)
        logging.info(
            f"Finished processing batch. Processed {len(all_command_outputs)} out of {len(managed_ids)}"
        )

    return all_command_outputs


def generate_excel_report(df, output_path):
    """
    Writes the final report to an Excel file.
    """
    try:
        with pd.ExcelWriter(output_path) as writer:
            df.to_excel(writer, sheet_name="AWS User Audit", index=False)
        logging.info(f"Report saved to: {output_path}")
    except Exception as e:
        logging.error(f"Failed to write Excel report: {e}")


def main():
    instance_details = get_instance_details()

    if not instance_details:
        logging.error("No instance details found. Exiting.")
        return []

    all_user_data = {}
    for platform in PLATFORMS:
        user_data = fetch_user_data(
            document_name=DOCUMENT, commands=COMMANDS, platform=platform
        )

        if not user_data:
            logging.error(f"No audit data retrieved for {platform}. Exiting.")

        all_user_data.update(user_data)

    for instance in instance_details:
        instance_id = instance["InstanceID"]
        instance["Users"] = all_user_data.get(instance_id, "-")

    report_date = datetime.today().strftime("%Y_%m_%d")

    # output_path = os.path.expanduser(
    #     f"/home/ahan/Documents/TTN/Code/Bootcamp/Boto3/aws_user_audit/files/AWS_User_Audit_{report_date}.xlsx"
    # )

    output_path = os.path.expanduser(
        f"~/aws_user_audit/AWS_User_Audit_{report_date}.xlsx"
    )

    audit_data_df = pd.DataFrame(instance_details)

    generate_excel_report(audit_data_df, output_path)


if __name__ == "__main__":
    main()


"""
aws ssm describe-instance-information \
  --filters "Key=InstanceIds,Values=i-011b451d9e0250a5f" \
"""
"""
aws ssm describe-instance-information \
  --filters "Key=InstanceIds,Values=i-03af62567bf6dcc1f" \
"""
"""
i-011b451d9e0250a5f
i-03af62567bf6dcc1f
"""

# get platform -> get managed_ids -> return managed_ids -> run command -> return command id -> get command output
# main() -> pass platform list
