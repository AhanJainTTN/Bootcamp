import boto3

ec2_resource = boto3.resource("ec2")
ec2_client = boto3.client("ec2")


def create_instances(min_count, max_count):
    try:
        instances = ec2_resource.create_instances(
            ImageId="ami-0e35ddab05955cf57",
            MinCount=min_count,
            MaxCount=max_count,
            InstanceType="t2.micro",
            KeyName="key-pair-20250411",
        )
        print(f"Successfully created EC2 instance(s): {instances}")
    except Exception as e:
        print(f"Error creating instances: {str(e)}")


def start_instances(instance_ids):
    try:
        response = ec2_client.start_instances(
            InstanceIds=instance_ids,
        )
        print(f"Instance(s) started successfully: {response["StartingInstances"]}")
    except Exception as e:
        print(f"Error starting instances: {str(e)}")


def stop_instances(instance_ids):
    try:
        response = ec2_client.stop_instances(
            InstanceIds=instance_ids,
        )
        print(f"Instance(s) stopped successfully: {response["StoppingInstances"]}")
    except Exception as e:
        print(f"Error stopping instance(s): {str(e)}")


def terminate_instances(instance_ids):
    try:
        response = ec2_client.terminate_instances(InstanceIds=instance_ids)
        print(f"Instance(s) terminated successfully: {response}")
    except Exception as e:
        print(f"Error terminating instance. {str(e)}")


def get_instance_details(instance_ids):
    try:
        response = ec2_client.describe_instances(
            InstanceIds=instance_ids,
        )
        print(response["Reservations"])
    except Exception as e:
        print(f"Error starting instances: {str(e)}")


def list_instances(status=None, terminated=False):
    filters = []

    if status:
        filters.append({"Name": "instance-state-name", "Values": status})
    elif not terminated:
        filters.append(
            {
                "Name": "instance-state-name",
                "Values": [
                    "pending",
                    "running",
                    "stopping",
                    "stopped",
                    "shutting-down",
                ],
            }
        )

    instances = (
        ec2_resource.instances.filter(Filters=filters)
        if filters
        else ec2_resource.instances.all()
    )

    return {instance.id: instance.state["Name"] for instance in instances}


if __name__ == "__main__":

    instances = list_instances()
    print(instances)

    # create_instances(3, 3)

    instances = list_instances()
    print(instances)

    instance_ids = list(instances.keys())
    print(instance_ids)

    # get_instance_details(instance_ids)
    # stop_instances(list(list_instances(status=["running"]).keys()))
    # start_instances(list(list_instances(status=["stopped"]).keys()))
    # terminate_instances(instance_ids)
