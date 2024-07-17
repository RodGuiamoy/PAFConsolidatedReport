import requests
import time
import sys
from datetime import datetime


def generate_token(azure_client_id, azure_client_secret):

    azure_client_id = azure_client_id
    azure_client_secret = azure_client_secret

    data = {
        "scope": "https://management.azure.com/.default",
        "grant_type": "client_credentials",
        "client_id": azure_client_id,
        "client_secret": azure_client_secret,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(
        "https://login.microsoftonline.com/44ecf5c5-5945-4f24-96ec-a73db8335538/oauth2/v2.0/token",
        headers=headers,
        data=data,
    )
    bearer_token = response.json()["access_token"]

    return bearer_token

domain = sys.argv[1]
subscription_id = sys.argv[2]
resource_group = sys.argv[3]
ad_server_name = sys.argv[4]
s3_upload_url = sys.argv[5]
azure_client_id = sys.argv[6]
azure_client_secret = sys.argv[7]


base_url = "https://management.azure.com"

new_token = generate_token(azure_client_id, azure_client_secret)

api_version = "2023-09-01"
headers = {"Authorization": f"Bearer {new_token}", "Content-Type": "application/json"}

# Get the current date
current_date = datetime.now()

# Format the date to MMddyyyy
formatted_date = current_date.strftime("%m%d%Y")

# Using str.replace() to remove spaces
domain = domain.replace(" ", "")

# Define the CSV file name
csv_file_name = f"AD{domain}_{formatted_date}.csv"

# Load the PowerShell script from a file
with open("Get-AzureActiveDirectoryUsers.ps1", "r") as file:
    powershell_script = file.read()
    
# Define your additional PowerShell command to append
additional_command = f'''
Invoke-Main -s3UploadUrl "{s3_upload_url}" -outputFile "{csv_file_name}"
'''

# Append the command to the existing script
powershell_script += additional_command

post_data = {"commandId": "RunPowerShellScript", "script": [powershell_script]}
post_url = f"{base_url}/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Compute/virtualMachines/{ad_server_name}/runCommand?api-version={api_version}"
location = ""

# Initiate the command execution
while not location:
    try:
        run_init_response = requests.post(post_url, headers=headers, json=post_data)
        if run_init_response.status_code == 200 or run_init_response.status_code == 202:
            location = run_init_response.headers.get("Location", "")
    except Exception as e:
        print(f"Error initiating command: {e}")
    time.sleep(5)  # Retry after a short delay

if not location:
    print("\n=======================================================")
    print(f"RunCommand not sent successfully in {resource_group.upper()}!")
    print("=======================================================")
    sys.exit()
    
else:
    print("\n=======================================================")
    print(f"RunCommand sent successfully in {resource_group.upper()}!")
    print("=======================================================")
    print("Waiting for async call to finish...")

# Wait for the async call to finish and collect results
run_result_response = []
while True:
    try:
        result_response = requests.get(location, headers=headers)
        if result_response.status_code == 200:
            run_result_response = result_response.json().get("value", [])
            if run_result_response:
                break
        elif result_response.status_code == 202:
            print("still waiting...")
        else:
            print(f"Unexpected status code: {result_response.status_code}")
    except Exception as e:
        print(f"Error fetching command result: {e}")
    time.sleep(10)  # Check every 10 seconds


# Process and display the results
script_result = ""
if run_result_response:
    for result in run_result_response:
        script_result += result.get("message", "")

print("Result from PowerShell script:")
print(script_result)



# # Initialize a Boto3 session
# session = boto3.Session(region_name=region)

# # Use the SSM (Simple Systems Manager) client
# ssm = session.client("ssm")
# s3 = session.client("s3")

# s3.download_file(s3_bucket, csv_file_name, csv_file_name)

# with open(csv_file_name, "rb") as file:
#     for line in file:
#         print(line, end="")
