$option = $args[0]
$port = 8888

function Help {
    Write-Host "Chrome-Passwords-Manager"
    Write-Host "Decrypt the Google Chrome stored passwords in your computer"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "    --help  -h  Display help"
    Write-Host "    --web   -w  Run flask app to view the decrypted passwords"
}

function Start-Flask-App {
    python app.py $port
}

function Print-Decrypted {
    python decrypter\decrypter.py
}

if ($option -eq "-h" -or $option -eq "--help") {
    Help
} elseif ($option -eq "-w" -or $option -eq "--web") {
    Start-Flask-App
} else {
    Print-Decrypted
}