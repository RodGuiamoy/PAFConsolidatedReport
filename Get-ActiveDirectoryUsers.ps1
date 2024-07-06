$properties = 'SamAccountName', 'EmailAddress', 'EmployeeID', 'LastLogonDate'
$headers = ($properties -join ",") + ',Domain,OU,GroupMemberships'

$adUsers = Get-ADUser -Filter * -Properties $properties
$domain = (Get-CimInstance Win32_ComputerSystem).Domain

$userList = ""

$adUsers | % {

    $user = $_

    $propertyValues = @()

    foreach ($prop in $properties) {
        $propertyValues += "$($user.$prop)"
    }

    # Join all property value strings with a comma
    $outputString = $propertyValues -join ","

    # Get the OU from the DistinguishedName
    $ou = $user.DistinguishedName -replace '^.*?,(?=[A-Z]{2}=)'
    # Get the group memberships
    $groupNames = (Get-ADPrincipalGroupMembership $user | Select-Object Name).Name -join ","
        
    # Write-Host $outputString + ",$domain,`"$ou`",`"$groupNames`""
    $userList = ($userList + $outputString + ",$domain,`"$ou`",`"$groupNames`"`n")

    # Read-Host
}

$headers
$userList