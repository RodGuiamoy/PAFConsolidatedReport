import boto3
import csv
import sys

# Initialize boto3 clients
iam = boto3.client('iam')

def get_user_tags(username):
    """Retrieve user tags and return EmployeeID and Email if available."""
    tags = iam.list_user_tags(UserName=username)['Tags']
    employee_id = next((tag['Value'] for tag in tags if tag['Key'] == 'employeeID'), None)
    email = next((tag['Value'] for tag in tags if tag['Key'] == 'email'), None)
    return employee_id, email

def main(aws_environment):
    users = iam.list_users()['Users']
    account_id = boto3.client('sts').get_caller_identity().get('Account')
    
    # Define the CSV file name
    csv_file_name = f"AWS_{aws_environment}.csv"
    
    # Define the header names based on the data we are collecting
    headers = ['UserName', 'EmployeeID', 'Email', 'CreateDate', 'AccountID']
    
    # Open a new CSV file
    with open(csv_file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        
        # Write the header
        writer.writeheader()
        
        # Iterate over each user and write their information as a row in the CSV
        for user in users:
            username = user['UserName']
            employee_id, email = get_user_tags(username)
            created_date = user['CreateDate'].strftime('%Y-%m-%d %H:%M:%S')
            
            # Write the user's details to the CSV
            writer.writerow({
                'UserName': username,
                'EmployeeID': employee_id,
                'Email': email,
                'CreateDate': created_date,
                'AccountID': account_id
            })
            
            print (f"{username},{employee_id},{email},{created_date},{account_id}")

if __name__ == "__main__":
    aws_environment = sys.argv[1]
    main(aws_environment)
    
