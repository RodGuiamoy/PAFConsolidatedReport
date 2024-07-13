$properties = 'SamAccountName', 'EmailAddress', 'EmployeeID', 'LastLogonDate', 'MemberOf', 'DistinguishedName'

$adUsers = Get-ADUser -Filter * -Properties $properties
$domain = (Get-CimInstance Win32_ComputerSystem).Domain

$adUsersProcessed = $adUsers | `
    Select-Object @{Name = 'Domain'; Expression = { $domain } }, 'SamAccountName', 'EmailAddress', 'EmployeeID', 'LastLogonDate', @{Name = 'GroupMemberships'; Expression = { $_.MemberOf -join "; " } }, @{Name = 'OU'; Expression = { $_.DistinguishedName -replace '^.*?,(?=[A-Z]{2}=)' } }

# Assuming $object is your object
$finalProperties = ($adUsersProcessed | Get-Member -MemberType NoteProperty ).Name 
$finalProperties -join ","

$adUsersProcessed | % {
    $user = $_
    
    $finalPropertyValues = @()
    foreach ($prop in $finalProperties) {
        $finalPropertyValues += "$($user.$prop)"
    }

    $finalPropertyValues -join ","
}
