$properties = 'SamAccountName', 'EmailAddress', 'EmployeeID'
$headers = 'Domain,' + $($properties -join ",")
Write-Host "$headers"

$adUsers = Get-ADUser -Filter * -Properties $properties
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