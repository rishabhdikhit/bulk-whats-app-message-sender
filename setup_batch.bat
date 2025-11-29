@echo off
echo ============================================================
echo WhatsApp Bulk Sender - Setup Script
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is NOT installed!
    echo.
    echo Opening Python download page...
    echo Please download and install Python 3.x
    echo IMPORTANT: Check "Add Python to PATH" during installation
    echo.
    start https://www.python.org/downloads/
    echo.
    echo After installing Python, run this setup.bat again
    pause
    exit
)

echo Python is installed!
echo.
echo Installing required packages...
echo ============================================================
echo.

REM Install required packages
pip install selenium
pip install webdriver-manager

echo.
echo ============================================================
echo Installation Complete!
echo ============================================================
echo.
echo Next steps:
echo 1. Edit contacts.csv with your contact details
echo 2. Run run_sender.bat to start sending messages
echo.
pause