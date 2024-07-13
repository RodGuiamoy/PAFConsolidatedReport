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


domain = sys.argv[1]
region = sys.argv[2]
instance_id = sys.argv[3]

# Initialize a Boto3 session
session = boto3.Session(region_name=region)

# Use the SSM (Simple Systems Manager) client
ssm = session.client("ssm")
s3 = session.client("s3")

# need to add code to verify s3 bucket
target_bucket = f"infrasre-adreport-raw-{domain.lower()}"

# Get the current date
current_date = datetime.now()

# Format the date to MMddyyyy
formatted_date = current_date.strftime("%m%d%Y")

# Using str.replace() to remove spaces
domain = domain.replace(" ", "")

# Define the CSV file name
csv_file_name = f"AD{domain}_{formatted_date}.csv"

# Define the PowerShell script you want to run
# Load the PowerShell script from a file
with open("Get-AWSActiveDirectoryUsers.ps1", "r") as file:
    powershell_script = file.read()

# Define your additional PowerShell command to append
additional_command = f'''
Invoke-Main -BucketName "{target_bucket}" -CSVFileName "{csv_file_name}"
'''

# Append the command to the existing script
powershell_script += additional_command

# Send the command
response = ssm.send_command(
    InstanceIds=[instance_id],
    DocumentName="AWS-RunPowerShellScript",
    Parameters={"commands": [powershell_script], "executionTimeout": ["3600"]},
    TimeoutSeconds=300 #,
    #OutputS3BucketName=target_bucket,
)

# Extract command ID
command_id = response["Command"]["CommandId"]

# Wait for the command to complete and display the output
invocation_response = wait_for_command_to_complete(instance_id, command_id)

# output = invocation_response['StandardOutputContent'].splitlines()
# print(output)

# error = invocation_response['StandardErrorContent'].splitlines()
# print(error)

s3.download_file(target_bucket, csv_file_name, csv_file_name)

with open(csv_file_name, "rb") as file:
    for line in file:
        print(line, end="")
