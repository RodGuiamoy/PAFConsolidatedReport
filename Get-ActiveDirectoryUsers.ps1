$properties = 'SamAccountName', 'DisplayName', 'EmailAddress', 'AccountExpirationDate'
$adUsers = Get-ADUser -Filter * -Properties $properties
$adUsers | % {
    $user = $_
    $properties | % {
        $property = $_
        Write-Host "$($user.$property)," -NoNewline
    }
    Write-Host
}