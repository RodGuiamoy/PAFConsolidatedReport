Function Invoke-Main {
    Param(
        $s3UploadUrl
    )

    $properties = 'SamAccountName', 'EmailAddress', 'EmployeeID', 'LastLogonDate', 'MemberOf', 'DistinguishedName'

    $adUsers = Get-ADUser -Filter * -Properties $properties
    $domain = (Get-CimInstance Win32_ComputerSystem).Domain

    # Remove-Item "$domain.csv" -Force

    $adUsers | `
        Select-Object @{Name = 'Domain'; Expression = { $domain } }, 'SamAccountName', 'EmailAddress', 'EmployeeID', 'LastLogonDate', @{Name='GroupMemberships'; Expression = { $_.MemberOf -join "; "}}, @{Name = 'OU'; Expression = { $_.DistinguishedName -replace '^.*?,(?=[A-Z]{2}=)' } } | `
        Export-CSV $CSVFileName -NoTypeInformation -Encoding UTF8

    $cmd = 'curl -X PUT -T "{0}" --ssl-no-revoke "{1}"' -f "$domain.csv", $s3UploadUrl
    cmd /c $cmd
}