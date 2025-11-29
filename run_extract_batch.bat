@echo off
echo ============================================================
echo WhatsApp Replied Contacts Extractor
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please run setup.bat first
    echo.
    pause
    exit
)

echo Starting extractor...
echo.
echo IMPORTANT: Do NOT open any messages before running this!
echo The script will find all chats with unread message indicators.
echo.
pause

python extract_replied.py

pause