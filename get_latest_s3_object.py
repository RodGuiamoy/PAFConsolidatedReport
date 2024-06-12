import boto3
import sys
from datetime import datetime

def download_latest_s3_object(bucket_name, folder_name, file_name):
    s3 = boto3.client('s3')

    # List objects within the specified folder
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
    
    # Check if there are any objects in the folder
    if 'Contents' not in response:
        print("No objects found in the specified folder.")
        return

    # Get the latest object based on the LastModified attribute
    latest_object = max(response['Contents'], key=lambda x: x['LastModified'])
    
    latest_object_key = latest_object['Key']
    latest_object_last_modified = latest_object['LastModified']

    print(f"Latest object key: {latest_object_key}")
    print(f"Last modified: {latest_object_last_modified}")

    # Download the latest object
    s3.download_file(bucket_name, latest_object_key, file_name)

    print(f"Downloaded {latest_object_key} to {file_name}")

# # Replace these variables with your S3 bucket name, folder name, and download path
# bucket_name = 'rguiamoy-public'
# folder_name = 'test/'  # Ensure this ends with a '/'
# download_path = 'download_test.txt'

if __name__ == "__main__":
    bucket_name = sys.argv[1]
    folder_name = sys.argv[2]
    user_report_name = sys.argv[3]
    
        # Get the current date
    current_date = datetime.now()

    # Format the date to MMddyyyy
    formatted_date = current_date.strftime('%m%d%Y')
    
    # Define the CSV file name
    file_name = f"{user_report_name}_{formatted_date}.csv"
    
    download_latest_s3_object(bucket_name, folder_name, file_name)
