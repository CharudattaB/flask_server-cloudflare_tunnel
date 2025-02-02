@echo off

:: uninstalling cloudflared tunnel
echo Uninstalling Cloudflare Tunnel...
winget uninstall --id Cloudflare.cloudflared


:: Install Cloudflare Tunnel
echo Installing Cloudflare Tunnel...
:: Get the current directory of the batch file and store it in a variable
set SCRIPT_DIR=%~dp0

:: Run the setup from the same directory as the batch file
"%SCRIPT_DIR%cloudflared-windows-amd64.msi"
# this is a comment

:: Run the Python app
echo Starting app...
start cmd /k "python app.py"

:: Expose port using Cloudflare Tunnel (assumes port 5000 for Flask)
start cmd /k "cloudflared tunnel --url http://localhost:5000"
