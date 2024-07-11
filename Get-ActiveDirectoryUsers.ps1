$properties = 'SamAccountName', 'EmailAddress', 'EmployeeID'#, 'LastLogonDate', 'MemberOf'
$headers = 'Domain,' + ($properties -join ",") #+ ',OU,GroupMemberships'

$adUsers = Get-ADUser -Filter * -Properties $properties
$domain = (Get-CimInstance Win32_ComputerSystem).Domain

$userList = ""

$adUsers | % {

    $user = $_


    # # Get the OU from the DistinguishedName
    # $ou = $user.DistinguishedName -replace '^.*?,(?=[A-Z]{2}=)'

    # $groupMemberships = $user.MemberOf -join ";"
        
    #$userList = ($userList + "$domain," + "$($user.SamAccountName),$($user.EmailAddress),$($user.EmployeeID),$($user.LastLogonDate)," + "`"$ou`",`"$groupMemberships`"`n")
    $userList = ($userList + "$domain," + "$($user.SamAccountName),$($user.EmailAddress),$($user.EmployeeID)" + "`n")

}

$headers
$userList