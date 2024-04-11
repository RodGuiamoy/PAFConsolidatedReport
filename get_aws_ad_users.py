import boto3
import time
import sys

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

region = sys.argv[1]
instance_id = sys.argv[2]

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
print(invocation_response['StandardOutputContent'])

