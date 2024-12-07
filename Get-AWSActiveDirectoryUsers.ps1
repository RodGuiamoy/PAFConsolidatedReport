Function Invoke-Main {
    Param(
        $BucketName,
        $CSVFileName
    )

    $properties = 'Name', 'SamAccountName', 'EmailAddress', 'EmployeeID', 'LastLogonDate', 'MemberOf', 'DistinguishedName', 'whenCreated', 'whenChanged'

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

    Write-S3Object -BucketName $BucketName -File $CSVFileName 
}