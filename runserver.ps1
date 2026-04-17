$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir
$python = Join-Path $scriptDir 'venv\Scripts\python.exe'
& $python (Join-Path $scriptDir 'manage.py') runserver
