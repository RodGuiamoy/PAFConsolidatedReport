import boto3

# Initialize boto3 clients
iam = boto3.client('iam')
cloudtrail = boto3.client('cloudtrail')

def get_user_tags(username):
    """Retrieve user tags and return EmployeeID and Email if available."""
    tags = iam.list_user_tags(UserName=username)['Tags']
    employee_id = next((tag['Value'] for tag in tags if tag['Key'] == 'employeeID'), None)
    email = next((tag['Value'] for tag in tags if tag['Key'] == 'email'), None)
    return employee_id, email

def main():
    users = iam.list_users()['Users']
    account_id = boto3.client('sts').get_caller_identity().get('Account')
    
    user_details_lines = []
    for user in users:
        # print(user)
        # input()
        username = user['UserName']
        employee_id, email = get_user_tags(username)
        created_date = user['CreateDate'].strftime('%Y-%m-%d %H:%M:%S')
        
        user_details_lines.append(
            #f"{username},{employee_id},{email},{created_date},{last_activity_str},{account_id}"
            f"{username},{employee_id},{email},{created_date},{account_id}"
        )
    
    # Join the lines into a single multi-line string and print
    output = "\n".join(user_details_lines)
    print(output)

if __name__ == "__main__":
    main()
