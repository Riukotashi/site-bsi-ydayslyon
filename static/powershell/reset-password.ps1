param ([String]$server, [String]$password, [String]$username)
try {
    $password_sec = (ConvertTo-SecureString -AsPlainText $password -Force)
    Set-ADAccountPassword -Identity $username -Reset -NewPassword $password_sec -Server $server
}
catch {
    Write-Error $Error[0]
    Write-Error "file_user n'est pas valide"
    exit
}