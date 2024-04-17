import requests
import sys
from datetime import datetime
import csv

azure_client_id = sys.argv[1]
azure_client_secret = sys.argv[2]
azure_tenant = sys.argv[3]
tenant_id = sys.argv[4]

data = {
"scope":"https://graph.microsoft.com/.default",
"grant_type":"client_credentials",
"client_id":azure_client_id,
"client_secret":azure_client_secret
}

headers = {'Content-Type': 'application/x-www-form-urlencoded'}
response = requests.post(f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token", headers=headers, data=data)
bearer_token = response.json()['access_token']

cont = True
full_user_list = []
target_query_url = "https://graph.microsoft.com/v1.0/users"
headers = {'Authorization': f'Bearer {bearer_token}'}

while cont:

    response = requests.get(target_query_url, headers=headers).json()

    if "@odata.nextLink" in response.keys():
        target_query_url = response['@odata.nextLink']
    else:
        cont = False

    full_user_list.extend(response['value'])

# Get the current date
current_date = datetime.now()

# Format the date to MMddyyyy
formatted_date = current_date.strftime('%m%d%Y')

# Define the CSV file name
csv_file_name = f"AZ{azure_tenant}_{formatted_date}.csv"

# Define column headers that match the dictionary keys
headers = [
    "businessPhones","displayName", "givenName", "id", "jobTitle", "mail",
    "mobilePhone", "officeLocation", "preferredLanguage", "surname", "userPrincipalName"
]

# Open a new CSV file
with open(csv_file_name, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    
    # Write the header
    writer.writeheader()
    
    for user in full_user_list:
        
        # Process 'businessPhones' list to a string representation
        user['businessPhones'] = ', '.join(user['businessPhones']) if user['businessPhones'] else None
        writer.writerow(user)