$properties = 'SamAccountName', 'EmailAddress', 'EmployeeID'
$headers = 'Domain,' + $($properties -join ",")
Write-Host "$headers"

$adUsers = Get-ADUser -Filter * -Properties $properties
$domain = (Get-CimInstance Win32_ComputerSystem).Domain

$adUsers | % {

    $user = $_

    $propertyValues = @()

    foreach ($prop in $properties) {
        $propertyValues += "$($user.$prop)"
    }

    # Join all property value strings with a comma and space
    $outputString = $propertyValues -join ","
    
    Write-Host "$domain," -NoNewline
    Write-Host $outputString
}