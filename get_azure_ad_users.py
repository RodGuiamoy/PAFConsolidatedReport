import requests
import time
import boto3
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
azure_client_id = sys.argv[5]
azure_client_secret = sys.argv[6]

base_url = "https://management.azure.com"

new_token = generate_token(azure_client_id, azure_client_secret)

api_version = "2023-09-01"

headers = {"Authorization": f"Bearer {new_token}", "Content-Type": "application/json"}

# Define the PowerShell script you want to run
# Load the PowerShell script from a file
with open("Get-AzureActiveDirectoryUsers.ps1", "r") as file:
    powershell_script = file.read()

post_data = {"commandId": "RunPowerShellScript", "script": [powershell_script]}

post_url = f"{base_url}/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Compute/virtualMachines/{ad_server_name}/runCommand?api-version={api_version}"
location = ""

while not location:
    try:
        run_init_response = requests.post(post_url, headers=headers, json=post_data)
        location = run_init_response.headers["Location"]
    except:
        pass

run_result_response = ""

if location:
    print("\n=======================================================")
    print(f"RunCommand sent successfully in {resource_group.upper()}!")
    print("=======================================================")

    print("Waiting for async call to finish...")
    while not requests.get(location, headers=headers).text:
        print("still waiting...")
        time.sleep(10)

    run_result_response = requests.get(location, headers=headers).json()["value"]

    # ad_users = run_result_response[0]["message"]
    
    # print(run_result_response)
    ad_users = ""
    if run_result_response:
    
        for result in run_result_response:
            ad_users += result.get("message", "")
            
    print("Result from PowerShell script:")
    print(ad_users)

    
else:
    print("\n=======================================================")
    print(f"RunCommand not sent successfully in {resource_group.upper()}!")
    print("=======================================================")
    exit()

# Get the current date
current_date = datetime.now()

# Format the date to MMddyyyy
formatted_date = current_date.strftime("%m%d%Y")

# Using str.replace() to remove spaces
domain = domain.replace(" ", "")

# Define the CSV file name
csv_file_name = f"AD{domain}_{formatted_date}.csv"

# Open the file in write mode ('w' mode), this will create the file if it doesn't exist
# If the file already exists, it will be overwritten
with open(csv_file_name, "w") as file:
    # Write the content of the string variable to the file
    file.write(ad_users)

# set_expiry_and_tag(sys.argv[1],sys.argv[2], sys.argv[3], sys.argv[4])
