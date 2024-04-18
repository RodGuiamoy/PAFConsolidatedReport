from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
import azure.mgmt.compute.models as compute_models
import sys

# Azure setup - ensure you replace these with your actual details
subscription_id = sys.argv[1]
resource_group = sys.argv[2]
vm_name = sys.argv[3]
location = sys.argv[4]  # e.g., 'eastus'

# Service Principal/Managed Identity credentials
credential = DefaultAzureCredential()

# Initialize the Compute Management Client
compute_client = ComputeManagementClient(credential, subscription_id)

# PowerShell script you want to run
ps_script = """
Write-Output "Hello, this is a test from PowerShell"
Get-Process | Where-Object {$_.ProcessName -like "powershell"}
"""

# Configuring the PowerShell script to run on the VM
run_command_parameters = compute_models.RunCommandInput(
    command_id='RunPowerShellScript',  # For PowerShell scripts
    script=[ps_script]
)

# Execute the PowerShell script
run_command_result = compute_client.virtual_machines.begin_run_command(
    resource_group_name=resource_group,
    vm_name=vm_name,
    parameters=run_command_parameters
).result()

# Print the output of the PowerShell script
print("PowerShell script output:")
for message in run_command_result.value:
    print(message.message)
