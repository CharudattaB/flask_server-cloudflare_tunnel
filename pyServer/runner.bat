@echo off
set APP_FILE=app.py
set APP_PORT=5000
set CLOUDFLARED_PATH=cloudflared.exe

:: Check if cloudflared exists
if not exist "%CLOUDFLARED_PATH%" (
    echo cloudflared.exe not found. Please download it from:
    echo https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/
    pause
    exit /b
)

:: Start the Python app
echo Starting %APP_FILE%...
start cmd /k "python %APP_FILE%"

:: Expose the port with Cloudflare Tunnel
echo Exposing port %APP_PORT% using Cloudflare Tunnel...
start cmd /k "%CLOUDFLARED_PATH% tunnel --url http://localhost:%APP_PORT%"

pause
