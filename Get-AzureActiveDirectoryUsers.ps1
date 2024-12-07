Function Invoke-Main {
    Param(
        $s3UploadUrl,
        $CSVFileName
    )

    $properties = 'Name', 'SamAccountName', 'EmailAddress', 'EmployeeID', 'LastLogonDate', 'MemberOf', 'DistinguishedName', 'Description', 'whenCreated', 'whenChanged'

    $adUsers = Get-ADUser -Filter * -Properties $properties
    $domain = (Get-CimInstance Win32_ComputerSystem).Domain

    # Remove-Item "$domain.csv" -Force

    $adUsers | `
        Select-Object @{Name = 'Domain'; Expression = { $domain } }, `
        Name, SamAccountName, EmailAddress, EmployeeID, Description, LastLogonDate, `
        @{Name = 'CreatedDate'; Expression = { $_.whenCreated } }, `
        @{Name = 'ModifiedDate'; Expression = { $_.whenChanged } }, `
        @{Name = 'GroupMemberships'; Expression = { $_.MemberOf -join "; " } }, `
        @{Name = 'OU'; Expression = { $_.DistinguishedName -replace '^.*?,(?=[A-Z]{2}=)' } }, `
        @{Name = 'AccountStatus'; Expression = { if ($_.Enabled -eq $True) { 'Enabled' } else { 'Disabled' } } } | `
        Export-CSV $CSVFileName -NoTypeInformation -Encoding UTF8

    $cmd = 'curl -X PUT -T "{0}" --ssl-no-revoke "{1}"' -f $CSVFileName, $s3UploadUrl
    cmd /c $cmd

    Remove-Item $CSVFileName

}