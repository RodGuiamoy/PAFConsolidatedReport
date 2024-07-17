import boto3
import sys

s3_bucket = sys.argv[1]
object = sys.argv[2]

def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    # Generate a presigned URL for the S3 object
    s3_client = boto3.client("s3")
    try:
        response = s3_client.generate_presigned_url(
            "put_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )
    except Exception as e:
        print(e)
        return None

    # The response contains the presigned URL
    return response


# Example usage
url = create_presigned_url(s3_bucket, object)
print(url)

# curl -X PUT -T "{0}" --ssl-no-revoke "{1}"' -f "$domain.csv", $S3PresignedUploadUrl
