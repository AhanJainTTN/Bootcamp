import boto3

REGION = "ap-south-1"

ec2 = boto3.resource("ec2")


def create_instances():
    try:
        instances = ec2.create_instances(
            ImageId="",
            MinCount=1,
            MaxCount=1,
            InstanceType="t2.micro",
            KeyName="KeyPair1",
        )
    except Exception as e:
        print(f"Error creating instances: {str(e)}")


def launch_instance():
    pass


def list_all_instances():
    pass


def delete_instance():
    pass


if __name__ == "__main__":
    pass
