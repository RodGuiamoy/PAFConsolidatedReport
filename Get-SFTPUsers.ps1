Function Get-EFTFTPUsers {
    param(
        [string]$ComputerName = 'localhost',
        [pscredential]$Credential
    )

    $SFTPServer = New-Object -COM "SFTPCOMInterface.CIServer"
    $SFTPServer.Connect($ComputerName, 1100, $Credential.Username, $Credential.GetNetworkCredential().Password)
    $SFTPSites = $SFTPServer.Sites()

    $userList = @()
    # $properties = 'Server','Site','UserName','FullName','Email','IsEnabled','LastConnectionTime','AccountCreationTime'
    for ($i = 0; $i -lt $SFTPSites.Count(); $i++) {

        $site = $SFTPSites.Item($i)
        $users = $site.GetUsers()
    
        foreach ($user in $users) {
            $userSettings = $site.GetUserSettings($user)

            # $Enabled = $null
            
            $userProperties = [PSCustomObject]@{
                Server = $ENV:COMPUTERNAME
                Site = $site.Name
                UserName = $user
                Email = $userSettings.Email
                IsEnabled = $userSettings.GetEnableAccount([ref]$null)
                LastConnectionTime = $userSettings.LastConnectionTime
                AccountCreationTime = $userSettings.AccountCreationTime
            
            }

            $userList += $userProperties
        }
    }

    return $userList
}

Function Invoke-Main {
    Param(
        $UserName,
        $Pwrd
    )

    # Convert the plaintext password to a secure string
    $securePassword = ConvertTo-SecureString $Pwrd -AsPlainText -Force

    # Create the PSCredential object
    $credential = New-Object System.Management.Automation.PSCredential ($username, $securePassword)

    # Output the PSCredential object
    $userList = Get-EFTFTPUsers -Credential $credential

    # Get headers from the first object
    $headers = $userList[0].PSObject.Properties | Select-Object -ExpandProperty Name

    # Create a string to store the output
    $output = ($headers -join ",") + "`n"

    # Iterate through each object in the array
    foreach ($object in $userList) {
        # Get property values as a comma-separated string
        $values = $object.PSObject.Properties | ForEach-Object { $_.Value }
        # $line = ($headers -join ", ") + "`n" + ($values -join ", ")
        $line = $values -join ","
        $output += "$line`n"
    }

    # Output the formatted result
    Write-Output $output
}