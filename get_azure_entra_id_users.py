import requests
import sys

azure_client_id = sys.argv[1]
azure_client_secret = sys.argv[2]
tenant_id = sys.argv[3]

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
    
print(full_user_list)