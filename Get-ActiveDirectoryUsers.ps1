$properties = 'SamAccountName', 'EmailAddress', 'EmployeeID'
$adUsers = Get-ADUser -Filter * -Properties $properties | Where-Object EmailAddress -ne $null
$adUsers | % {
    $user = $_
    $properties | % {
        $property = $_
        Write-Host "$($user.$property)," -NoNewline
    }
    Write-Host
}