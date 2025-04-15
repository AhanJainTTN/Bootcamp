import os
import boto3

REGION = "ap-south-1"
MEDIA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "s3", "{bucket_name}"
)
SAMPLE_MEDIA_DIR = os.path.join(os.path.expanduser("~"), "sample_files")

s3_resource = boto3.resource("s3")


def upload_folder(bucket_name, folder):
    """Uploads all files to S3 Bucket while retaining the folder structure."""

    folder = os.path.abspath(folder)
    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            file_key = os.path.relpath(file_path, start=os.path.dirname(folder))
            upload_to_bucket(bucket_name, file_path, file_key)


def upload_to_bucket(bucket_name, file_path, file_key=None):

    if not file_key:
        file_key = os.path.basename(file_path)

    try:
        s3_resource.Bucket(bucket_name).upload_file(Filename=file_path, Key=file_key)
        print(f"{file_key} uploaded successfully.")
    except Exception as e:
        print(f"Error uploading {file_key}: {str(e)}")


def download_from_bucket(bucket_name, file_keys):
    if not isinstance(file_keys, list):
        raise TypeError("Invalid type for file_keys. List expected.")

    for file_key in file_keys:
        try:
            local_dir = os.path.join(
                MEDIA_DIR.format(bucket_name=bucket_name), os.path.dirname(file_key)
            )
            os.makedirs(local_dir, exist_ok=True)
            local_path = os.path.join(local_dir, os.path.basename(file_key))

            if not os.path.exists(local_path):
                s3_resource.Bucket(bucket_name).download_file(file_key, local_path)
                print(f"{file_key} downloaded to {local_path}.")
            else:
                print(f"{file_key} already exists at {local_path}.")

        except Exception as e:
            print(f"Error downloading {file_key}: {str(e)}")


def delete_from_bucket(bucket_name, file_keys):
    try:
        if not isinstance(file_keys, list):
            raise TypeError("Invalid type for file_keys. List expected.")

        bucket = s3_resource.Bucket(bucket_name)
        objects = [{"Key": key} for key in file_keys]
        response = bucket.delete_objects(Delete={"Objects": objects})
        deleted = [obj["Key"] for obj in response.get("Deleted", [])]
        errors = response.get("Errors", [])
        print(f"Deleted: {deleted}")
        if errors:
            print(f"Errors: {errors}")
    except (TypeError, Exception) as e:
        print(f"Batch deletion failed: {str(e)}")


def get_bucket_objects(bucket_name):
    return [fileobj.key for fileobj in s3_resource.Bucket(bucket_name).objects.all()]


def create_bucket(s3_resource, bucket_name, region=REGION):
    try:
        create_bucket_response = s3_resource.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": region},
        )
        print(f"Bucket '{bucket_name}' created successfully. {create_bucket_response}")
    except Exception as e:
        print(f"Error creating bucket {bucket_name}: {str(e)}.")


def delete_all_buckets(s3_resource):
    for bucket_name in list_buckets(s3_resource):
        delete_bucket(s3_resource, bucket_name)


def delete_bucket(s3_resource, bucket_name):
    try:
        bucket = s3_resource.Bucket(bucket_name)
        bucket.delete()
        print(f"Bucket '{bucket_name}' deleted successfully.")
    except Exception as e:
        print(f"Error deleting bucket {bucket_name}: {str(e)}")


def list_buckets(s3_resource):
    return [bucket.name for bucket in s3_resource.buckets.all()]


if __name__ == "__main__":

    print(list_buckets(s3_resource))
    bucket_name = "test-bucket-boto3-20250410"

    bucket_objects = get_bucket_objects(bucket_name)
    print(bucket_objects)

    delete_from_bucket(bucket_name, bucket_objects)
    print(get_bucket_objects(bucket_name))

    # upload_folder(bucket_name, SAMPLE_MEDIA_DIR)
    # print(get_bucket_objects(bucket_name))
