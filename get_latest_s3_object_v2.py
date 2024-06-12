import boto3
import botocore
import logging
import re
import sys
from datetime import datetime

def download_latest_s3_object(bucket_name, folder_name, regex_pattern, output_filename):
    s3 = boto3.client("s3")
    
    try:
        # List all objects in the bucket
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
        
        # Check if there are any objects in the bucket
        if "Contents" not in response:
            print("No objects found in the specified bucket.")
            return
        
        # print(response["Contents"])
        
        # Compile the regex pattern
        pattern = re.compile(f"{folder_name}{regex_pattern}")
        
        # Filter objects using the regex pattern
        filtered_objects = [obj for obj in response["Contents"] if pattern.match(obj["Key"])]
        
        if not filtered_objects:
            print("No objects match the specified pattern.")
            return
        
        # Get the latest object based on the LastModified attribute
        latest_object = max(filtered_objects, key=lambda x: x["LastModified"])
        
        latest_object_key = latest_object["Key"]
        latest_object_last_modified = latest_object["LastModified"]
        
        print(f"Latest object key: {latest_object_key}")
        print(f"Last modified: {latest_object_last_modified}")
        
        # Download the latest object
        s3.download_file(bucket_name, latest_object_key, output_filename)
        
        print(f"Downloaded {latest_object_key} to {output_filename}")
    
    except botocore.exceptions.ClientError as e:
        logging.error(e)
        print(f"Failed to download the latest object due to an error: {e}")
    except Exception as e:
        logging.error(e)
        print(f"An unexpected error occurred: {e}")

# Example usage
#download_latest_s3_object('rguiamoy-public', r'test/test.*', 'test.txt')

if __name__ == "__main__":
    bucket_name = sys.argv[1]
    folder_name = sys.argv[2]
    regex_pattern = sys.argv[3]
    user_report_name = sys.argv[4]

    # Get the current date
    current_date = datetime.now()

    # Format the date to MMddyyyy
    formatted_date = current_date.strftime("%m%d%Y")

    # Define the CSV file name
    output_filename = f"{user_report_name}_{formatted_date}.csv"

    download_latest_s3_object(bucket_name, folder_name, regex_pattern, output_filename)
