Function Invoke-Main {
    Param(
        $CSVFileName
    )

    $properties = 'SamAccountName', 'EmailAddress', 'EmployeeID', 'LastLogonDate', 'MemberOf', 'DistinguishedName'

    $adUsers = Get-ADUser -Filter * -Properties $properties
    $domain = (Get-CimInstance Win32_ComputerSystem).Domain

    # Remove-Item "$domain.csv" -Force

    $adUsers | `
        Select-Object @{Name = 'Domain'; Expression = { $domain } }, 'SamAccountName', 'EmailAddress', 'EmployeeID', 'LastLogonDate', @{Name='GroupMemberships'; Expression = { $_.MemberOf -join "; "}}, @{Name = 'OU'; Expression = { $_.DistinguishedName -replace '^.*?,(?=[A-Z]{2}=)' } } | `
        Export-CSV $CSVFileName -NoTypeInformation -Encoding UTF8

    Write-S3Object -BucketName infrasre-adreport-raw-avitru -File $CSVFileName 
}