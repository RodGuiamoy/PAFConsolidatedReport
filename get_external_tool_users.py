import sys
import requests
import time
import csv
import json
from sendgrid import SendGridAPIClient

def get_pingdom_users(api_key):
    base_url = "https://api.pingdom.com/api/3.1/alerting/contacts"
    headers = {"Authorization":f"Bearer {api_key}"}

    user_list = requests.get(base_url, headers=headers).json()
    
    # Define the CSV file name
    csv_file_name = f"Pingdom.csv"

    # Define the header names based on the data we are collecting
    headers = ['id', 'name', 'email']
    # Open a new CSV file
    with open(csv_file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        
        # Write the header
        writer.writeheader()
        
        # Iterate over each user and write their information as a row in the CSV
        for user in user_list['contacts']:
            id = user['id']
            name = user['name']
            email = user['notification_targets']['email'][0]['address']
            
            # Write the user's details to the CSV
            writer.writerow({
                'id': id,
                'name': name,
                'email': email
            })
            
            print(f"{id}, {name}, {email}")

def get_pagerduty_users(api_key):
   
    base_url = "https://api.pagerduty.com/users"
    headers = {
	    "Content-Type": "application/json",
	    "Authorization": f"Token token={api_key}"
	}
	
    offset = 0
    params = {
		"limit":100,
		"offset":offset
	}

    response = requests.get(base_url, headers=headers, params=params).json()
    user_list = response['users'].copy()
	
	#loop get requests since results are paginated
    while response['more']==True:
        time.sleep(1)
        offset += 100
        params['offset'] = offset
        response = requests.get(base_url, headers=headers, params=params).json()
        user_list.extend(response['users'])
        
    # Define the CSV file name
    csv_file_name = f"PagerDuty.csv"
 
    # Define the header names based on the data we are collecting
    headers = ['id', 'name', 'email']
    # Open a new CSV file
    with open(csv_file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        
        # Write the header
        writer.writeheader()
        
        # Iterate over each user and write their information as a row in the CSV
        for user in user_list:
            id = user['id']
            name = user['name']
            email = user['email']
            
            # Write the user's details to the CSV
            writer.writerow({
                'id': id,
                'name': name,
                'email': email
            })
            
            print(f"{id}, {name}, {email}")    
              
def get_sendgrid_users(api_key):
    
    sg = SendGridAPIClient(api_key)
    response = sg.client.teammates.get(query_params={'limit': 500})
    user_list = json.loads(response.body)['result']
    
    # Define the CSV file name
    csv_file_name = f"Sendgrid.csv"
 
    # Define the header names based on the data we are collecting
    headers = ['username', 'email']
    # Open a new CSV file
    with open(csv_file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        
        # Write the header
        writer.writeheader()
        
        # Iterate over each user and write their information as a row in the CSV
        for user in user_list:
            username = user['name']
            email = user['email']
            
            # Write the user's details to the CSV
            writer.writerow({
                'username': username,
                'email': email
            })
            
            print(f"{username}, {email}")    
    
def get_site24x7_users(api_key):
    return api_key
def get_duo_users(api_key):
    return api_key
def default_case():
    return "There is no function created to retrieve users from this environment."

external_tool_name = sys.argv[1]
api_key = sys.argv[2]
api_key = api_key.replace("\n","").strip()

# Define the switch-case dictionary
external_tool_functions = {
    "Pingdom": get_pingdom_users,
    "PagerDuty": get_pagerduty_users,
    "SendGrid": get_sendgrid_users,
    "Site24x7": get_site24x7_users,
    "DUO": get_duo_users
}

# Check if choice exists in the dictionary
if external_tool_name in external_tool_functions:
    # Call the function corresponding to the choice
    external_tool_functions[external_tool_name](api_key)
else:
    # If choice doesn't exist, call the default case function
    default_case()   