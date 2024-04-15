import boto3
import time
import sys
#import csv
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

domain = sys.argv[1]
region = sys.argv[2]
instance_id = sys.argv[3]

# Initialize a Boto3 session
session = boto3.Session(region_name=region)

# Use the SSM (Simple Systems Manager) client
ssm = session.client('ssm')
s3 = session.client('s3')

# Define the PowerShell script you want to run
# Load the PowerShell script from a file
with open('Get-ActiveDirectoryUsers.ps1', 'r') as file:
    powershell_script = file.read()

# need to add code to verify s3 bucket
target_bucket = f'infrasre-adreport-raw-{domain.lower()}'

# Send the command
response = ssm.send_command(
    InstanceIds=[instance_id],
    DocumentName='AWS-RunPowerShellScript',
    Parameters={'commands': [powershell_script]},
    TimeoutSeconds=300,
    OutputS3BucketName=target_bucket
)

# Extract command ID
command_id = response['Command']['CommandId']

# Wait for the command to complete and display the output
invocation_response = wait_for_command_to_complete(instance_id, command_id)
ad_users_str = invocation_response['StandardOutputContent'].splitlines()

# Get the current date
current_date = datetime.now()

# Format the date to MMddyyyy
formatted_date = current_date.strftime('%m%d%Y')

# Using str.replace() to remove spaces
domain = domain.replace(" ", "")

# Define the CSV file name
csv_file_name = f"AD{domain}_{formatted_date}.csv"

# Define the header names based on the data we are collecting
headers = 'Domain,SamAccountName,EmailAddress,EmployeeID\n'

#get output from s3
# s3_client = boto3.client('s3')
s3_download_path = f'{command_id}/{instance_id}/awsrunPowerShellScript/0.awsrunPowerShellScript/stdout'
s3.download_file(target_bucket, s3_download_path, csv_file_name)

# Step 1: Read the existing content
with open(csv_file_name, 'rb') as file:
    original_content = file.readlines()

# Step 2: Convert original_content from list to string if necessary
original_content = ''.join(original_content)  # Joins all elements of the list into a single string

# Step 3: Add the header line at the beginning
new_content = headers + original_content

# Step 3: Write the updated content back to the file
with open(csv_file_name, 'w') as file:
    file.writelines(new_content)
    
print(new_content)

# Open a new CSV file
#with open(csv_file_name, mode='w', newline='') as file:
    # writer = csv.DictWriter(file, fieldnames=headers)
    
    # # Write the header
    # writer.writeheader()

    # for ad_user in ad_users_str:
    #     ad_user_properties = ad_user.split(',')
        
    #     # Initialize variables with None or default values
    #     sam_account_name = None
    #     # display_name = None
    #     email = None
    #     employee_id = None

    #     # Conditional assignments
    #     if ad_user_properties[0].strip():
    #         sam_account_name = ad_user_properties[0].strip()
    #     if len(ad_user_properties) > 1 and ad_user_properties[1].strip():
    #         email = ad_user_properties[1].strip()
    #     if len(ad_user_properties) > 2 and ad_user_properties[2].strip():
    #         employee_id = ad_user_properties[2].strip()
    #     # if len(ad_user_properties) > 3 and ad_user_properties[3].strip():
    #     #     account_expiration_date = ad_user_properties[3].strip()
        
    #     # Write the user's details to the CSV
    #     writer.writerow({
    #         'Domain': domain,
    #         'SamAccountName': sam_account_name,
    #         'EmailAddress': email,
    #         'EmployeeID': employee_id
    #     })
        
    #     # print(f"{domain},{sam_account_name},{display_name},{email},{account_expiration_date}")
    #     print(f"{domain},{sam_account_name},{email},{employee_id}")

    

