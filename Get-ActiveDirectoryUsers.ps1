$properties = 'SamAccountName', 'EmailAddress', 'EmployeeID'
$adUsers = Get-ADUser -Filter * -Properties $properties | Where-Object EmailAddress -ne $null
$domain = (Get-CimInstance Win32_ComputerSystem).Domain

$adUsers | % {
    $user = $_
    
    Write-Host "$domain," -NoNewline

    $properties | % {
        $property = $_
        Write-Host "$($user.$property)," -NoNewline
    }
    Write-Host
}