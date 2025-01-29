@echo off

:: Check if Python is installed; if not, install it
where python >nul 2>nul
if errorlevel 1 (
    echo Installing Python...
    curl -o python-installer.exe "https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe"
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python-installer.exe
)

:: Install pip dependencies
python -m ensurepip
python -m pip install --upgrade pip
pip install flask

:: Install Cloudflare Tunnel
echo Installing Cloudflare Tunnel...
winget install --id Cloudflare.cloudflared


:: Run the Python app
echo Starting app...
start cmd /k "python app.py"

:: Expose port using Cloudflare Tunnel (assumes port 5000 for Flask)
start cmd /k "cloudflared tunnel --url http://localhost:5000"
