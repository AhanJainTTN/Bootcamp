import os
import json
import boto3
from botocore.exceptions import ClientError

ecs_client = boto3.client("ecs")
ec2_client = boto3.client("ec2")


def run_task(cluster_name: str, task_family: str, subnet_ids: list = None) -> dict:
    try:
        if not subnet_ids:
            vpcs = ec2_client.describe_vpcs(
                Filters=[{"Name": "isDefault", "Values": ["true"]}]
            )
            default_vpc_id = vpcs["Vpcs"][0]["VpcId"]

            subnets = ec2_client.describe_subnets(
                Filters=[{"Name": "vpc-id", "Values": [default_vpc_id]}]
            )
            subnet_ids = [subnet["SubnetId"] for subnet in subnets["Subnets"]][:1]

        task_definitions = ecs_client.list_task_definitions(
            familyPrefix=task_family, sort="DESC"
        )["taskDefinitionArns"]

        if not task_definitions:
            raise ValueError(
                f"No task definitions found for task family '{task_family}'."
            )

        latest_task_def = task_definitions[0]

        response = ecs_client.run_task(
            cluster=cluster_name,
            taskDefinition=latest_task_def,
            launchType="FARGATE",
            networkConfiguration={
                "awsvpcConfiguration": {
                    "subnets": subnet_ids,
                    "assignPublicIp": "ENABLED",
                }
            },
        )

        task_arn = response["tasks"][0]["taskArn"]
        print(f"Task started: {task_arn}")
        return response

    except Exception as e:
        print(f"Failed to run task: {e}")
        raise


def create_task(task_json_path: str) -> str:
    try:
        with open(task_json_path, "r") as f:
            task_def = json.load(f)

        response = ecs_client.register_task_definition(**task_def)
        family = response["taskDefinition"]["family"]
        revision = response["taskDefinition"]["revision"]
        print(f"Task definition registered: {family}:{revision}")
        return f"{family}:{revision}"

    except Exception as e:
        print(f"Failed to register task definition: {e}")
        raise


def create_cluster(cluster_name: str = "fargate-cluster") -> str:
    try:
        response = ecs_client.create_cluster(clusterName=cluster_name)
        print(f"Cluster created: {response['cluster']['clusterArn']}")
        return response["cluster"]["clusterArn"]
    except ClientError as e:
        print(f"Failed to create cluster: {e}")
        raise


def list_clusters():
    response = ecs_client.list_clusters()["clusterArns"]
    print("Available clusters:", response)
    return response


def describe_clusters(cluster_arn):
    response = ecs_client.describe_clusters(clusters=[cluster_arn])
    cluster_name = response["clusters"][0]["clusterName"]
    print(f"Using cluster: {cluster_name}")
    return cluster_name


if __name__ == "__main__":
    # cluster_name = create_cluster("TestClusterBoto3")
    # task_def_path = os.path.join(
    #     os.path.dirname(os.path.dirname(__file__)),
    #     "sample_files",
    #     "hello-world-runner-boto3.json",
    # )
    # task = create_task(task_def_path)

    cluster_name = describe_clusters(list_clusters()[0])
    task = "HelloWorldRunner"
    # task = "HelloWorldRunnerBoto3"

    run_task(cluster_name, task)
