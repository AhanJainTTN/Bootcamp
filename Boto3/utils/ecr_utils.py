import boto3

ecr_client = boto3.client("ecr")


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

    print(
        {
            "ID": response.get("registryId"),
            "Name": response.get("repositoryName"),
            "URI": response.get("repositoryUri"),
        }
    )


# Flow: Build image if it does not exist -> Get credentials -> Tag image -> Upload to ECR
def upload_image(
    image,
    repository_name,
    image_tag=None,
    path_to_dockerfile=None,
    build=False,
):
    """Runs commands to build, tag and push Docker image to AWS registry."""
    registry_uri = describe_repository(repository_name).get("URI")

    if build:
        build_cmd = f"docker build -t {image}:{image_tag if image_tag else "latest"} {path_to_dockerfile}"

    creds_cmd = f"aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin {registry_uri}"
    tag_cmd = f"docker tag {image}:{image_tag} {registry_uri}:{image_tag}"
    push_cmd = f"docker push {registry_uri}:{image_tag}"


"""
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin {registry_uri}
if build: docker build -t {image_name}:{image_tag} {path_to_dockerfile}
docker tag {image_name}:{image_tag} {registry_uri}:{image_tag}
docker push {registry_uri}:{image_tag}
"""

if __name__ == "__main__":
    # create_repository("test-boto3-deploy")
    list_images("test-boto3-deploy")
    describe_repository("test-boto3-deploy")
