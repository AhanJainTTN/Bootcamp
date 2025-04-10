import os
import boto3

REGION = "ap-south-1"
MEDIA_DIR = "/home/ahan/Documents/Bootcamp/Boto3/s3/{bucket_name}/"
SAMPLE_MEDIA_DIR = "/home/ahan/Documents/sample_files/"

s3_resource = boto3.resource("s3")


def upload_to_bucket(bucket_name, file_path, file_key=None):

    if not file_key:
        file_key = os.path.basename(file_path)

    try:
        s3_resource.Bucket(bucket_name).upload_file(Filename=file_path, Key=file_key)
        print(f"{file_key} uploaded successfully.")
    except Exception as e:
        print(f"Error uploading {file_key}: {str(e)}")


def download_from_bucket(bucket_name, file_key):
    try:
        local_dir = os.path.join(
            MEDIA_DIR.format(bucket_name=bucket_name), os.path.dirname(file_key)
        )
        os.makedirs(local_dir, exist_ok=True)
        local_path = os.path.join(local_dir, os.path.basename(file_key))

        if not os.path.exists(local_path):
            s3_resource.Bucket(bucket_name).download_file(file_key, local_path)
            print(f"{file_key} downloaded to {local_dir}.")

    except Exception as e:
        print(f"Error downloading {file_key}: {str(e)}")


def delete_from_bucket(bucket_name, file_key):
    try:
        s3_resource.Object(bucket_name, file_key).delete()
        print(f"{file_key} deleted successfully.")
    except Exception as e:
        print(f"Error deleting {file_key}: {str(e)}")


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

    bucket_name = "test-bucket-boto3-20250410"

    print(list_buckets(s3_resource))

    print(get_bucket_objects(bucket_name))

    file_path = "/home/ahan/Documents/sample_files/text_files/long-doc.txt"
    upload_to_bucket(bucket_name, file_path)
    print(get_bucket_objects(bucket_name))

    download_from_bucket(bucket_name, "long-doc.txt")

    delete_from_bucket(bucket_name, "long-doc.txt")
    print(get_bucket_objects(bucket_name))
