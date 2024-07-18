import boto3
from botocore.exceptions import NoCredentialsError
from datetime import datetime, timedelta
import sys


def upload_file_to_s3(file_name, bucket_name, object_name=None):
    """Upload a file to an S3 bucket and generate a presigned URL.

    :param file_name: File to upload
    :param bucket_name: S3 bucket to upload to
    :param object_name: S3 object name. If not specified, file_name is used
    :return: Presigned URL as string. If error, returns None.
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Create an S3 client
    s3_client = boto3.client("s3")

    try:
        # Upload the file
        s3_client.upload_file(file_name, bucket_name, object_name)
    except FileNotFoundError:
        print("The file was not found")
        return None
    except NoCredentialsError:
        print("Credentials not available")
        return None

    # Generate a presigned URL for the S3 object
    try:
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=7 * 24 * 60 * 60,
        )  # 7 days
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    # The response contains the presigned URL
    return response


# Usage example:
bucket_name = sys.argv[1]
file_name = sys.argv[2]

presigned_url = upload_file_to_s3(file_name, bucket_name, file_name)

if presigned_url:
    # print("File uploaded successfully!")
    print(presigned_url)
