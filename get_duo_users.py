# ------------------------------------------------------------------------
# ./delete_duo_user.py
# Michael Dennis M. Cresido, 02/07/2024
# This Python script is created to delete user account that are tagged
# in PAF. The input for this tool will be the e-mail address of the target
# user. It will then be executed in this duo client: "api-54f22240.duosecurity.com".
# All the information and log will be displayed in Jenkins 
# output log and will archived in S3.
#!/usr/bin/python3

# Initializing imports
from __future__ import absolute_import
from __future__ import print_function
import argparse
import pprint
import sys

import duo_client
import json
import os

# Initializing Global variables
email_list = open("temp_user.txt")
target_email = email_list.read()
target_email = target_email.strip()
target_email = target_email.replace("\n","")

api_id_file = open("temp_id.txt")
api_id = api_id_file.read()
api_id = api_id.replace("\n","")

api_secret_file = open("temp_secret.txt")
api_secret = api_secret_file.read()
api_secret = api_secret.replace("\n","")

# Initializing DUO API Client
duo_ikey = api_id
duo_skey = api_secret
du_host = "api-54f22240.duosecurity.com"
admin_api = duo_client.Admin(ikey=duo_ikey,skey=duo_skey,host=du_host)

# This is the actual delete function
def delete_function():
    
    # Retrieve all DUO users
    get_info = admin_api.get_users()
    
    # Display the total user count before deletion
    count = len(get_info)
    print("\n=======================================================")
    print(f"RunCommand sent successfully. Total user count before the deletion: ", count)
    print("=========================================================")
    try:
        # Deleting users with this e-mail address
        for i in range(len(get_info)):
            duo_email = (get_info[i]['email'])

            # Condition if the user account will be deleted if email_parameter is the with the account's duo e-mail
            if duo_email == target_email:
                # Retrieve user id. Parameter needed for the actual deletion.
                duo_userid = (get_info[i]['user_id'])
                info_username = (get_info[i]['username'])
                if duo_email == '':
                    print("No email value. Skipping this user," )

                else:
                    # Display all user information for logging purposes.
                    print("Displaying user information: ",get_info[i])
                    
                    # Command for deleting the user.
                    delete_info = admin_api.delete_user(user_id = duo_userid)
                    print("Username: ", info_username)
                    print("User was successfully deleted:", target_email)

    except Exception as e:
        pass
        print("Email address: " + target_email + " has an issue. Error message: ", e)
        
    after_info = admin_api.get_users()
    
    # Display the total user count after the activity.
    after_count = len(after_info)
    print("\n=======================================================")
    print(f"RunCommand sent successfully. Total user count after the deletion: ", after_count)
    print("=========================================================")


delete_function()
