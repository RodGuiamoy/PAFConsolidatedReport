import boto3
import csv
import sys
from datetime import datetime, timezone
import time

# Initialize boto3 clients
iam = boto3.client("iam")


def get_user_tags(username):
    """Retrieve user tags and return EmployeeID and Email if available."""
    tags = iam.list_user_tags(UserName=username)["Tags"]
    employee_id = next(
        (tag["Value"] for tag in tags if tag["Key"] == "employeeID"), None
    )
    email = next((tag["Value"] for tag in tags if tag["Key"] == "email"), None)
    return employee_id, email


def get_group_attached_policies(group_name):
    """Retrieve policies attached to a group."""
    attached_policies_response = iam.list_attached_group_policies(GroupName=group_name)
    attached_policies = [
        policy["PolicyName"]
        for policy in attached_policies_response["AttachedPolicies"]
    ]
    return attached_policies

def get_access_keys(username):
    try:
        # Get the access keys for the specified user
        access_keys = iam.list_access_keys(UserName=username)['AccessKeyMetadata']
        if not access_keys:
            result = "No access keys"
        else:
            result_lines = []
            for key in access_keys:
                
                access_key_id = key['AccessKeyId']
                status = key['Status']
                create_date = key['CreateDate']
                
                # Calculate the age of the access key
                current_time = datetime.now(timezone.utc)
                age_days = (current_time - create_date).days
                
                # Get the last used date of the access key
                last_used_response = iam.get_access_key_last_used(AccessKeyId=access_key_id)
                last_used_date = last_used_response['AccessKeyLastUsed'].get('LastUsedDate')
                if last_used_date:
                    last_used_days = (current_time - last_used_date).days
                    usage_info = f"Used {last_used_days} days ago"
                else:
                    usage_info = "Never used"
                
                result_lines.append(f"Access Key ID: {access_key_id}, Status: {status}, Usage: {usage_info}, Age: {age_days} days old")
            result = "\n".join(result_lines)
    except Exception as e:
        result = f"An error occurred: {e}"

    # print(result)
    return result

def get_mfa(username):
    # List MFA devices for the specified user
    response = iam.list_mfa_devices(UserName=username)

    # Extract and print the list of MFA devices
    mfa_devices = response.get('MFADevices', [])
    
    # Check if there are no MFA devices and return None if so
    if not mfa_devices:
        return None

    # Extract serial numbers and join them with a separator (e.g., ', ')
    serial_numbers = [device['SerialNumber'] for device in mfa_devices]
    serial_numbers_string = ', '.join(serial_numbers)

    # Print the serial numbers in one line
    return serial_numbers_string
    
def main(aws_environment):
    
    iam.attach_user_policy(UserName='sre-cli-user',PolicyArn="arn:aws:iam::aws:policy/AdministratorAccess")
    time.sleep(10)

    
    # users = iam.list_users()['Users']
    account_id = boto3.client("sts").get_caller_identity().get("Account")

    # Get the current date
    current_date = datetime.now()

    # Format the date to MMddyyyy
    formatted_date = current_date.strftime("%m%d%Y")

    # Using str.replace() to remove spaces
    aws_environment = aws_environment.replace(" ", "")

    # Define the CSV file name
    csv_file_name = f"AWS{aws_environment}_{formatted_date}.csv"

    # Define the header names based on the data we are collecting
    headers = [
        "AWSAccountID",
        "UserName",
        "EmployeeID",
        "Email",
        "CreateDate",
        "Groups",
        "GroupAttachedPolicies",
        "DirectlytAttachedPolicies",
        "InlinePolicies",
        "ConsoleAccess",
        "AccessKeys",
        "MFA"
    ]

    # Open a new CSV file
    with open(csv_file_name, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)

        # Write the header
        writer.writeheader()

        # Assuming iam is a configured AWS IAM client
        paginator = iam.get_paginator("list_users")
        for response in paginator.paginate():
            for user in response["Users"]:
                # # Iterate over each user and write their information as a row in the CSV
                # for user in users:
                username = user["UserName"]
                employee_id, email = get_user_tags(username)
                created_date = user["CreateDate"].strftime("%Y-%m-%d %H:%M:%S")

                # Get groups for the user
                groups_response = iam.list_groups_for_user(UserName=username)
                groups = [group["GroupName"] for group in groups_response["Groups"]]

                # Get attached policies for the user
                directly_attached_policies_response = iam.list_attached_user_policies(
                    UserName=username
                )
                directly_attached_policies = [
                    policy["PolicyName"]
                    for policy in directly_attached_policies_response[
                        "AttachedPolicies"
                    ]
                ]

                # Get inline policies for the user
                inline_policies_response = iam.list_user_policies(UserName=username)
                inline_policies = [
                    policy_name
                    for policy_name in inline_policies_response["PolicyNames"]
                ]

                # Get policies attached via groups for the user
                group_attached_policies = []
                for group_name in groups:
                    group_attached_policies.extend(
                        get_group_attached_policies(group_name)
                    )
                    
                # Get login profile to check console access
                try:
                    iam.get_login_profile(UserName=username)
                    console_access = True
                except iam.exceptions.NoSuchEntityException:
                    console_access = False
                    pass
                
                mfa = get_mfa(username)
                access_keys = get_access_keys(username)

                # Write the user's details to the CSV
                writer.writerow(
                    {
                        "AWSAccountID": account_id,
                        "UserName": username,
                        "EmployeeID": employee_id,
                        "Email": email,
                        "CreateDate": created_date,
                        "Groups": ",".join(groups),
                        "GroupAttachedPolicies": ",".join(group_attached_policies),
                        "DirectlytAttachedPolicies": ",".join(
                            directly_attached_policies
                        ),
                        "InlinePolicies": ",".join(inline_policies),
                        "ConsoleAccess": console_access,
                        "AccessKeys": access_keys,
                        "MFA": mfa
                    }
                )

                print(
                    f"{username},{employee_id},{email},{created_date},{','.join(groups)},{','.join(directly_attached_policies)},{','.join(inline_policies)},{','.join(group_attached_policies)},{account_id}"
                )

    iam.detach_user_policy(UserName='sre-cli-user',PolicyArn="arn:aws:iam::aws:policy/AdministratorAccess")

if __name__ == "__main__":
    aws_environment = sys.argv[1]
    main(aws_environment)
