import boto3
import time
import sys
import csv
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
        status = invocation_response['Status']
        if status not in ['Pending', 'InProgress', 'Delayed']:
            return invocation_response 

# region = 'ap-southeast-1'
# instance_id = 'i-077367418569315f2'

aws_ad_environment = sys.argv[1]
region = sys.argv[2]
instance_id = sys.argv[3]

# Initialize a Boto3 session
session = boto3.Session(region_name=region)

# Use the SSM (Simple Systems Manager) client
ssm = session.client('ssm')

# Define the PowerShell script you want to run
# Load the PowerShell script from a file
with open('Get-ActiveDirectoryUsers.ps1', 'r') as file:
    powershell_script = file.read()

# Send the command
response = ssm.send_command(
    InstanceIds=[instance_id],
    DocumentName='AWS-RunPowerShellScript',
    Parameters={'commands': [powershell_script]},
)

# Extract command ID
command_id = response['Command']['CommandId']

# Wait for the command to complete and display the output
invocation_response = wait_for_command_to_complete(instance_id, command_id)
adUsersStr = invocation_response['StandardOutputContent'].splitlines()


# Get the current date
current_date = datetime.now()

# Format the date to MMddyyyy
formatted_date = current_date.strftime('%m%d%Y')

# Using str.replace() to remove spaces
aws_ad_environment = aws_ad_environment.replace(" ", "")

# Define the CSV file name
csv_file_name = f"AD{aws_ad_environment}_{formatted_date}.csv"

# Define the header names based on the data we are collecting
headers = ['SamAccountName', 'DisplayName', 'EmailAddress', 'AccountExpirationDate']

# Open a new CSV file
with open(csv_file_name, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)

    for adUser in adUsersStr:
        adUserProperties = adUser.split(',')
        
        SamAccountName = adUserProperties[0]
        DisplayName = adUserProperties[1]
        Email = adUserProperties[2]
        AccountExpirationDate = adUserProperties[3]
        
        # Write the user's details to the CSV
        writer.writerow({
            'SamAccountName': SamAccountName,
            'DisplayName': DisplayName,
            'EmailAddress': Email,
            'AccountExpirationDate': AccountExpirationDate
        })
        
        print(f"{SamAccountName},{DisplayName},{Email},{AccountExpirationDate}")

    

