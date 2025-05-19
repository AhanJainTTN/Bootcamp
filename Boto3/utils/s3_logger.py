import json


def lambda_handler(event, context):
    event_details = event["Records"][0]
    action = event_details.get("eventName")
    s3_details = event_details.get("s3")
    bucket_details = s3_details.get("bucket").get("name")
    object_key = s3_details.get("object").get("key")

    response = {"Bucket": bucket_details, "Action": action, "Object": object_key}

    print(json.dumps(response))
    return response
