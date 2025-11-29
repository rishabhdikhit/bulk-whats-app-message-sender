@echo off
echo ============================================================
echo WhatsApp Bulk Message Sender
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

REM Check if contacts.csv exists
if not exist "contacts.csv" (
    echo ERROR: contacts.csv not found!
    echo.
    echo Please create contacts.csv with the following format:
    echo Name,Phone
    echo Sudhanshu Kumar,919876543210
    echo Naresh Prajapati,919876543211
    echo.
    pause
    exit
)

echo Starting WhatsApp Sender...
echo.
python whatsapp_sender.py

pause