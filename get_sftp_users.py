import boto3
import time
import sys

# import csv
from datetime import datetime

# Function to wait for command to complete and return the result
def wait_for_command_to_complete(instance_id, command_id):
    while True:
        # Wait for 5 seconds before checking again
        time.sleep(5)
        # Fetch the command invocation details
        invocation_response = ssm.get_command_invocation(
            CommandId=command_id,
            InstanceId=instance_id,
        )
        # Check if the command has completed
        status = invocation_response["Status"]
        if status not in ["Pending", "InProgress", "Delayed"]:
            return invocation_response

server_name = sys.argv[1]
instance_id = sys.argv[2]
region = sys.argv[3]
s3_bucket = sys.argv[4]
username = sys.argv[5]
password = sys.argv[6]


# Initialize a Boto3 session
session = boto3.Session(region_name=region)

# Use the SSM (Simple Systems Manager) client
ssm = session.client("ssm")
s3 = session.client("s3")

# Define the PowerShell script you want to run
# Load the PowerShell script from a file
with open("Get-SFTPUsers.ps1", "r") as file:
    powershell_script = file.read()
    
# Define your additional PowerShell command to append
additional_command = f'''
Invoke-Main -UserName "{username}" -Pwrd "{password}"
'''

# Append the command to the existing script
powershell_script += additional_command

# need to add code to verify s3 bucket
# target_bucket = f"infrasre-adreport-raw-{aws_environment.lower()}"
# target_bucket = f"infrasre-{aws_environment.lower()}-sftp-users-raw"


# Send the command
response = ssm.send_command(
    InstanceIds=[instance_id],
    DocumentName="AWS-RunPowerShellScript",
    Parameters={"commands": [powershell_script]},
    TimeoutSeconds=300,
    OutputS3BucketName=s3_bucket
)

# Extract command ID
command_id = response["Command"]["CommandId"]

# Wait for the command to complete and display the output
invocation_response = wait_for_command_to_complete(instance_id, command_id)
sftp_users = invocation_response["StandardOutputContent"] #.splitlines()

# Get the current date
current_date = datetime.now()

# Format the date to MMddyyyy
formatted_date = current_date.strftime("%m%d%Y")

# Define the CSV file name
csv_file_name = f"SFTP_{server_name}_{formatted_date}.csv"

# # Open file in write mode ('w'), will create the file if it doesn't exist
# with open(csv_file_name, 'w') as file:
#     file.write(sftp_users)
    
# print(sftp_users)

# get output from s3
s3_download_path = (
    f"{command_id}/{instance_id}/awsrunPowerShellScript/0.awsrunPowerShellScript/stdout"
)
s3.download_file(s3_bucket, s3_download_path, csv_file_name)

with open(csv_file_name, "rb") as file:
    for line in file:
        print(line, end="")