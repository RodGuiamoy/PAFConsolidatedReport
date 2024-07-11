Function Invoke-Main {
    Param(
        $S3PresignedUploadUrl
    )

    $properties = 'SamAccountName', 'EmailAddress', 'EmployeeID', 'LastLogonDate', 'MemberOf', 'DistinguishedName'

    $adUsers = Get-ADUser -Filter * -Properties $properties
    $domain = (Get-CimInstance Win32_ComputerSystem).Domain

    $adUsers | `
        Select-Object @{Name = 'Domain'; Expression = { $domain } }, 'SamAccountName', 'EmailAddress', 'EmployeeID', 'LastLogonDate', @{Name='GroupMemberships'; Expression = { $_.MemberOf -join "; "}}, @{Name = 'OU'; Expression = { $_.DistinguishedName -replace '^.*?,(?=[A-Z]{2}=)' } } | `
        Export-CSV "$domain.csv" -NoTypeInformation -Encoding UTF8

    $cmd = 'curl -X PUT -T "{0}" --ssl-no-revoke "{1}"' -f "$domain.csv", $S3PresignedUploadUrl
    cmd /c $cmd
}