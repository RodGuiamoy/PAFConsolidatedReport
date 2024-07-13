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

# base param set
# sub_id = "ca451cef-a9cc-4e8e-b9eb-f35f39fdac77"
# target_vm = "ADDC2"
api_version = "2023-09-01"
# resource_groups = ["productionprimary", "ProductionSecondary"]

headers = {"Authorization": f"Bearer {new_token}", "Content-Type": "application/json"}

# script is defined here

# post_data = {"commandId":"RunPowerShellScript","script":["# Get all users from Active Directory\r\n$allUsers = Get-ADUser -Filter * -Properties SamAccountName, DisplayName, EmailAddress, AccountExpirationDate, Title\r\n \r\n# required variables\r\n$emailInput = \""+target_email+"\"\r\n$newExpiryDate = \""+cutoffdate+"\"\r\n$newTitle = \"AutoExpireEnabled\"\r\n \r\n# Filter users based on the input email address\r\n$matchingUsers = $allUsers | Where-Object { $_.EmailAddress -eq $emailInput }\r\n \r\n# Check if any users were found\r\nif ($matchingusers -ne $null) {\r\n    # Display header before update\r\n    Write-Host \"Before Update - SamAccountName`tDisplayName`tEmailAddress`tAccountExpiry`tTitle\"\r\n \r\n    # Display user details before update\r\n    foreach ($user in $matchingUsers) {\r\n        $samAccountName = $user.SamAccountName\r\n        $displayName = $user.DisplayName\r\n        $emailAddress = $user.EmailAddress\r\n        $accountExpiry = $user.AccountExpirationDate\r\n        $title = $user.Title\r\n \r\n        Write-Host \"$samAccountName`t$displayName`t$emailAddress`t$accountExpiry`t$title\"\r\n    }\r\n \r\n    # Separate message\r\n    Write-Host \"---------------------\"\r\n    Write-Host \"Updating user attributes...\"\r\n \r\n \r\n    # Update account attributes\r\n    foreach ($user in $matchingUsers) {\r\n        $samAccountName = $user.SamAccountName\r\n \r\n        # Update account expiration date and title\r\n        Set-ADUser -Identity $samAccountName -AccountExpirationDate $newExpiryDate -Title $newTitle\r\n    }\r\n \r\n    Start-Sleep -Seconds 10\r\n \r\n    # Display header after update\r\n    Write-Host \"After Update - SamAccountName`tDisplayName`tEmailAddress`tAccountExpiry`tTitle\"\r\n \r\n    # Display user details after update\r\n    foreach ($user in $matchingUsers){\r\n    # Fetch the latest user details after the update\r\n    $updatedUser = Get-ADUser -Identity $user.SamAccountName -Properties SamAccountName, DisplayName, EmailAddress, AccountExpirationDate, Title\r\n     \r\n        $samAccountName = $updatedUser.SamAccountName\r\n        $displayName = $updatedUser.DisplayName\r\n        $emailAddress = $updatedUser.EmailAddress\r\n        $accountExpiry = $updatedUser.AccountExpirationDate\r\n        $title = $updatedUser.Title\r\n \r\n        Write-Host \"$samAccountName`t$displayName`t$emailAddress`t$accountExpiry`t$title\"\r\n    }\r\n} else {\r\n    Write-Host \"No users found with the provided email address.\"\r\n}"]}

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

    ad_users = run_result_response[0]["message"]
    
    print(run_result_response)
    
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
