import os
import base64
import boto3
import docker
from botocore.exceptions import ClientError

ecr_client = boto3.client("ecr")
docker_client = docker.from_env()


def list_images(repository_name):
    response = ecr_client.list_images(
        repositoryName=repository_name,
    )

    print(response.get("imageIds", []))


# Registries have repositories which have images.
def create_repository(repository_name):
    response = ecr_client.create_repository(
        repositoryName=repository_name,
    )

    print(response)


def describe_repository(repository_name):
    response = ecr_client.describe_repositories(repositoryNames=[repository_name])[
        "repositories"
    ][0]

    return {
        "ID": response.get("registryId"),
        "Name": response.get("repositoryName"),
        "URI": response.get("repositoryUri"),
    }


"""
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin {registry_uri}
if build: docker build -t {image_name}:{image_tag} {path_to_dockerfile}
docker tag {image_name}:{image_tag} {registry_uri}:{image_tag}
docker push {registry_uri}:{image_tag}
"""


# Flow: Build image if it does not exist -> Get credentials -> Tag image -> Upload to ECR
def upload_image(
    image_name,
    ecr_repository,
    tag="latest",
    dockerfile_path=None,
):
    try:
        # Check if the image exists locally
        docker_client.images.get(f"{image_name}:{tag}")
        print(f"Image '{image_name}:{tag}' already exists locally.")
    except docker.errors.ImageNotFound:
        if dockerfile_path:
            print(f"Building image from Dockerfile at {dockerfile_path}...")
            image, _ = docker_client.images.build(
                path=dockerfile_path, tag=f"{image_name}:{tag}"
            )
        else:
            raise ValueError("Image not found and no Dockerfile provided.")

    # Get URI
    try:
        repository_uri = describe_repository(ecr_repository).get("URI")
        print(repository_uri)
    except ClientError:
        print(f"Repository '{ecr_repository}' not found.")

    # Get ECR login
    print("Authenticating Docker with ECR...")
    auth_data = ecr_client.get_authorization_token()
    auth_data = auth_data["authorizationData"][0]
    ecr_url = auth_data["proxyEndpoint"]
    auth_token = auth_data["authorizationToken"]
    username, password = base64.b64decode(auth_token).decode("utf-8").split(":")

    docker_client.login(username=username, password=password, registry=ecr_url)

    # Tag image and push
    ecr_image_tag = f"{repository_uri}:{tag}"
    print(f"Tagging image as {ecr_image_tag}")
    docker_client.images.get(f"{image_name}:{tag}").tag(ecr_image_tag)

    print(f"Pushing image to {ecr_image_tag}...")
    for line in docker_client.images.push(ecr_image_tag, stream=True, decode=True):
        print(line)

    print("Image pushed successfully.")


if __name__ == "__main__":
    ecr_repository = "test-boto3-deploy"

    # create_repository(ecr_repository)
    list_images(ecr_repository)
    describe_repository(ecr_repository)

    # image_name = "hello-world-py"
    # dockerfile_path = os.path.join(
    #     os.path.dirname(os.path.dirname(__file__)),
    #     "docker_sample_ecr_test",
    # )

    # upload_image(
    #     image_name, ecr_repository, tag="latest", dockerfile_path=dockerfile_path
    # )
