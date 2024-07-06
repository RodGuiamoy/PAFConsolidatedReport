$properties = 'SamAccountName', 'EmailAddress', 'EmployeeID', 'LastLogonDate'
$headers = ($properties -join ",") + ',Domain,OU,GroupMemberships'
Write-Host "$headers"

$adUsers = Get-ADUser -Filter * -Properties $properties
$domain = (Get-CimInstance Win32_ComputerSystem).Domain

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
        
    Write-Host $outputString -NoNewline
    Write-Host ",$domain,`"$ou`",`"$groupNames`""

    # Read-Host
}
