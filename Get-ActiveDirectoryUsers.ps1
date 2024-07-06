#Measure-Command {
$properties = 'SamAccountName', 'EmailAddress', 'EmployeeID', 'LastLogonDate', 'MemberOf'
$headers = 'Domain,' + ($properties -join ",") + ',OU'
    
$adUsers = Get-ADUser -Filter * -Properties $properties
$domain = (Get-CimInstance Win32_ComputerSystem).Domain
    
$userList = ""
    
$adUsers | % {
    
    $user = $_
    
    $propertyValues = @()
    
    $properties | Where-Object { $_ -ne 'MemberOf' } | % {
        
        $propertyValues += $user.$_
    
    }
    
    # Join all property value strings with a comma
    $outputString = $propertyValues -join ","
    
    # Get the OU from the DistinguishedName
    $ou = $user.DistinguishedName -replace '^.*?,(?=[A-Z]{2}=)'
    
    $groupMemberships = $user.MemberOf -join "; "
            
    $userList = ($userList + "$domain," + $outputString + ",`"$groupMemberships`"" + ",`"$ou`"`n")
    
}
    
$headers
$userList
    