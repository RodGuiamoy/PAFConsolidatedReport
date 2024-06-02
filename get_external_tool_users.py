import sys
import requests
import time
import csv
import json
from sendgrid import SendGridAPIClient
from datetime import datetime
import duo_client

def get_pingdom_users(api_id, api_key):
    base_url = "https://api.pingdom.com/api/3.1/alerting/contacts"
    headers = {"Authorization":f"Bearer {api_key}"}

    user_list = requests.get(base_url, headers=headers).json()
    
    # Get the current date
    current_date = datetime.now()

    # Format the date to MMddyyyy
    formatted_date = current_date.strftime('%m%d%Y')
    
    # Define the CSV file name
    csv_file_name = f"Pingdom_{formatted_date}.csv"

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

def get_pagerduty_users(api_id, api_key):
   
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
    
    # Get the current date
    current_date = datetime.now()

    # Format the date to MMddyyyy
    formatted_date = current_date.strftime('%m%d%Y')
    
    # Define the CSV file name
    csv_file_name = f"PagerDuty_{formatted_date}.csv"
 
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
              
def get_sendgrid_users(api_id, api_key):
    
    sg = SendGridAPIClient(api_key)
    response = sg.client.teammates.get(query_params={'limit': 500})
    user_list = json.loads(response.body)['result']
    
    # Get the current date
    current_date = datetime.now()

    # Format the date to MMddyyyy
    formatted_date = current_date.strftime('%m%d%Y')
    
    # Define the CSV file name
    csv_file_name = f"Sendgrid_{formatted_date}.csv"
 
    # Define the header names based on the data we are collecting
    headers = ['username', 'email']
    # Open a new CSV file
    with open(csv_file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        
        # Write the header
        writer.writeheader()
        
        # Iterate over each user and write their information as a row in the CSV
        for user in user_list:
            username = user['username']
            email = user['email']
            
            # Write the user's details to the CSV
            writer.writerow({
                'username': username,
                'email': email
            })
            
            print(f"{username}, {email}")
    
def get_site24x7_users(api_id, api_key):
    params = {
		"client_id":api_id, 
		"client_secret":api_key,
		"grant_type":"client_credentials",
		"scope":"Site24x7.Account.All",
		"soid":"1000.843810594"
	}

    base_url = "https://accounts.zoho.com/oauth/v2/token"
    access_token = requests.post(base_url, params=params).json()['access_token']
    
    s247_url = "https://www.site24x7.com/api/users"
    list_headers = {
		"Accept":"application/json; version=2.0",
		"Authorization" : f"Zoho-oauthtoken {access_token}"
	}

    user_list = requests.get(s247_url, headers=list_headers).json()
    
    # Get the current date
    current_date = datetime.now()

    # Format the date to MMddyyyy
    formatted_date = current_date.strftime('%m%d%Y')
    
    # Define the CSV file name
    csv_file_name = f"Site24x7_{formatted_date}.csv"
 
    # Define the header names based on the data we are collecting
    headers = ['user_id', 'display_name', 'email_address']
    # Open a new CSV file
    with open(csv_file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        
        # Write the header
        writer.writeheader()
        
        # Iterate over each user and write their information as a row in the CSV
        for user in user_list['data']:
            user_id = user['user_id']
            display_name = user['display_name']
            email_address = user['email_address']
            
            # Write the user's details to the CSV
            writer.writerow({
                'user_id': user_id,
                'display_name': display_name,
                'email_address': email_address
            })
            
            print(f"{user_id}, {display_name}, {email_address}")
 
def get_duo_users(api_id, api_key):
    
    # Initializing DUO API Client
    duo_ikey = api_id
    duo_skey = api_key
    du_host = "api-54f22240.duosecurity.com"
    admin_api = duo_client.Admin(ikey=duo_ikey,skey=duo_skey,host=du_host)
    
    # Retrieve all DUO users
    user_list = admin_api.get_users()
    
    # Get the current date
    current_date = datetime.now()

    # Format the date to MMddyyyy
    formatted_date = current_date.strftime('%m%d%Y')
    
    # Define the CSV file name
    csv_file_name = f"DUO_{formatted_date}.csv"
 
    # Define the header names based on the data we are collecting
    headers = ['user_id', 'username', 'realname', 'status', 'email_address']
    # Open a new CSV file
    with open(csv_file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        
        # Write the header
        writer.writeheader()
        
        # Iterate over each dictionary in the list and print it
        for user in user_list:
            # try:
            #     # Convert dictionary to string
            #     info_str = str(info)
            #     print(info_str)
            # except Exception as e:
            #     # Catch and ignore any encoding errors
            #     print(f"Error printing info: {e}")
            #     print(info_str.encode('utf-8', errors='ignore').decode('utf-8'))
            
            user_id = user['user_id']
            username = user['username']
            realname = user['realname']
            status = user['status']
            email_address = user['email']
            
            # Write the user's details to the CSV
            writer.writerow({
                'user_id': user_id.encode('utf-8', errors='ignore').decode('utf-8'),
                'username': username.encode('utf-8', errors='ignore').decode('utf-8'),
                'realname': realname.encode('utf-8', errors='ignore').decode('utf-8'),
                'status': status.encode('utf-8', errors='ignore').decode('utf-8'),
                'email_address': email_address.encode('utf-8', errors='ignore').decode('utf-8')
            })
            
            print(f"{user_id}, {username}, {email_address}")            
    

    
    # return api_key    

external_tool_name = sys.argv[1]

api_id = sys.argv[2]
api_id = api_id.replace("\n","").strip()

api_key = sys.argv[3]
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
    external_tool_functions[external_tool_name](api_id, api_key)
else:
    print ("There is no function created to retrieve users from this environment.")