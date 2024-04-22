import sys
import requests
import time

def get_pingdom_users(api_key):
    return api_key
def get_pagerduty_users(api_key):
    print(api_key)
    
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
 
    return user_list

def get_sendgrid_users(api_key):
    return api_key
def get_site24x7_users(api_key):
    return api_key
def get_duo_users(api_key):
    return api_key
def default_case():
    return "There is no function created to retrieve users from this environment."

external_tool_name = sys.argv[1]
api_key = sys.argv[2]

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
    result = external_tool_functions[external_tool_name](api_key)
else:
    # If choice doesn't exist, call the default case function
    default_case()
    
print(result)