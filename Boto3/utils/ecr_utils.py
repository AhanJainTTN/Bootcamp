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
    response = ecr_client.describe_repositories(repositoryNames=[repository_name])

    print(
        response["repositories"][0]["registryId"],
        response["repositories"][0]["repositoryName"],
        response["repositories"][0]["repositoryUri"],
    )


def upload_image(image_path, exists=True):
    """Runs commands to build, tag and push d=Docker image to AWS registry."""
    pass


if __name__ == "__main__":
    # create_repository("test-boto3-deploy")
    list_images("test-boto3-deploy")
    describe_repository("test-boto3-deploy")
