param ([String]$server, [String]$username, [String]$fullname, [String]$firstname, [String]$lastname, [String]$ou, [String]$email, [String]$class)

function Get-RandomCharacters($length, $characters) {
    $random = 1..$length | ForEach-Object { Get-Random -Maximum $characters.length }
    $private:ofs=""
    return [String]$characters[$random]
}
 
function Scramble-String([string]$inputString){     
    $characterArray = $inputString.ToCharArray()   
    $scrambledStringArray = $characterArray | Get-Random -Count $characterArray.Length     
    $outputString = -join $scrambledStringArray
    return $outputString 
}
 
$password = Get-RandomCharacters -length 6 -characters 'abcdefghiklmnoprstuvwxyz'
$password += Get-RandomCharacters -length 3 -characters 'ABCDEFGHKLMNOPRSTUVWXYZ'
$password += Get-RandomCharacters -length 3 -characters '1234567890'
$password += Get-RandomCharacters -length 3 -characters '!"§$%&/()=?}][{@#*+'
 
$password = Scramble-String $password
$password_sec = (ConvertTo-SecureString -AsPlainText "$password" -Force)

try{
    New-ADUser -Server $server -SamAccountName $username -Name $fullname -GivenName $firstname -Surname $lastname -UserPrincipalName $username -Path $ou -AccountPassword $password_sec -Enabled $true -ChangePasswordAtLogon $false -EmailAddress $email -PasswordNotRequired $false -AccountNotDelegated $true -PasswordNeverExpires $true

    if ($class -ne "formateur") {
      Write-host "test"
      Add-ADGroupMember -Identity $class -Members $username
    }
    Write-host "222222"
}
catch {
    Write-Error $Error[0]
    Write-Error "file_user n'est pas valide"
    exit
}