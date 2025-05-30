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
DOCUMENTS = {"Linux": "AWS-RunShellScript", "Windows": "AWS-RunPowerShellScript"}
COMMANDS = {
    "Linux": ["getent passwd | awk -F: '/\/bin\/bash|\/bin\/false/ {print $1}'"],
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

        instance_details = {}
        for page in pages:
            for reservation in page["Reservations"]:
                for instance in reservation["Instances"]:
                    instance_id = instance["InstanceId"]

                    # Skip if IP starts with 100.
                    private_ip = instance.get("PrivateIpAddress", "100.")
                    if private_ip.startswith("100."):
                        logging.info(
                            f"Skipping {instance_id} due to internal IP {private_ip}"
                        )
                        continue

                    platform = instance.get("PlatformDetails", "Other")
                    state = instance["State"]["Name"]

                    # Extract Name tag
                    name = ""
                    for tag in instance.get("Tags", []):
                        if tag["Key"] == "Name":
                            name = tag["Value"]
                            break

                    instance_details[instance_id] = {
                        "InstanceID": instance_id,
                        "Name": name,
                        "Platform": platform.split("/")[0],
                        "State": state,
                        "Users": "-",
                    }

        return instance_details

    except (BotoCoreError, ClientError) as e:
        logging.error(f"Failed to describe EC2 instances: {e}")
        return []


def run_ssm_command(instance_ids, document_name, commands, platform):
    """
    Sends SSM command to the given instance IDs using the specified document.
    """
    parameters = {"commands": commands[platform]}

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

        return response.get("StandardOutputContent")

    except ssm.exceptions.InvocationDoesNotExist as e:
        logging.warning(f"Output not yet available for {instance_id}: {e}")
        raise
    except (BotoCoreError, ClientError) as e:
        logging.error(f"Error fetching output for {instance_id}: {e}")
        return None


def get_ssm_managed_instance_details(platform):
    """
    Returns a details of managed instance IDs for a specified platform which have Online PingStatus
    and registered with SSM.
    """
    paginator = ssm.get_paginator("describe_instance_information")
    pages = paginator.paginate(Filters=[{"Key": "PlatformTypes", "Values": [platform]}])

    managed_instances = {}
    for page in pages:
        for info in page["InstanceInformationList"]:
            instance_id = info.get("InstanceId")

            # Skip if IP starts with 100.
            ip_address = info.get("IPAddress", "100.")
            if ip_address.startswith("100."):
                logging.error(f"Skipping {instance_id} due to internal IP: {ip_address}")
                continue

            instance_name = info.get("ComputerName").split(".")[0]
            ping_status = info.get("PingStatus")

            if (
                instance_id
                and ping_status
                and ping_status == "Online"
            ):
                managed_instances[instance_id] = {
                    "InstanceID": instance_id,
                    "Name": instance_name,
                    "Platform": platform,
                    "State": "running",
                    # "State": ping_status,
                    "Users": "-",
                }

            else:
                logging.error(
                    f"Instance is registered under SSM but not reachable: {instance_id}"
                )

    return managed_instances


def process_batch(managed_ids, command_id, max_wait, poll_interval):
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

                if instance_id.startswith("m"):
                    logging.info(command_output)

                # there exists a small window where it is possible where a command output exists but it is blank
                # get_command_output will not raise an error but return a blank output
                # solution is to just wait and get it in the next polling interval
                # so it makes sense for instance to be added to te set only if command_output exists
                if command_output:
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
    max_wait=60,  # max wait time to process a batch
    poll_interval=4,  # time between retries for a single batch
):
    """
    Starts the user info retrieval across all instances for a particular platform.
    """
    logging.info(f"Started retrieval for {platform} instances")

    # get all ids which are online and registered
    managed_instance_details = get_ssm_managed_instance_details(platform=platform)
    managed_ids = list(managed_instance_details.keys())

    all_command_outputs = {}
    for batch in batch_process(managed_ids, batch_size):

        # get command id for output retrieval
        command_id = run_ssm_command(batch, document_name, commands, platform=platform)

        if not command_id:
            logging.error(f"Failed to process batch.")
            continue

        command_ouputs = process_batch(
            batch, command_id, max_wait=max_wait, poll_interval=poll_interval
        )
        all_command_outputs.update(command_ouputs)
        logging.info(
            f"Finished processing batch. Processed {len(all_command_outputs)} out of {len(managed_ids)}"
        )

    for instance_id in all_command_outputs.keys():
        managed_instance_details[instance_id]["Users"] = all_command_outputs.get(
            instance_id
        )

    return managed_instance_details


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
        document_name = DOCUMENTS[platform]
        user_data = fetch_user_data(
            document_name=document_name, commands=COMMANDS, platform=platform
        )

        if not user_data:
            logging.error(f"No audit data retrieved for {platform}. Exiting.")

        all_user_data.update(user_data)

    for instance_id in all_user_data.keys():
        if instance_id not in instance_details:
            instance_details[instance_id] = all_user_data[instance_id]
            continue

        instance_details[instance_id]["Users"] = all_user_data[instance_id]["Users"]

    report_date = datetime.today().strftime("%Y_%m_%d")
    output_path = os.path.expanduser(
        f"~/aws_user_audit/AWS_User_Audit_{report_date}.xlsx"
    )

    audit_data_df = pd.DataFrame(instance_details.values())

    generate_excel_report(audit_data_df, output_path)


if __name__ == "__main__":
    main()
