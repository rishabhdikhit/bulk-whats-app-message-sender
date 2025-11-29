============================================================
WHATSAPP BULK MESSAGE SENDER - COMPLETE GUIDE
============================================================

📁 FOLDER STRUCTURE
-------------------
Create a new folder (e.g., "WhatsApp_Sender") and place these files:

WhatsApp_Sender/
├── setup.bat              (Run this FIRST)
├── run_sender.bat         (Run this to send messages)
├── whatsapp_sender.py     (Main Python script)
├── contacts.csv           (Your contact list - EDIT THIS)
└── README.txt             (This file)


🚀 STEP-BY-STEP INSTALLATION
-----------------------------

STEP 1: Create the folder
   - Create a new folder on your Desktop called "WhatsApp_Sender"

STEP 2: Save all files
   - Copy all 5 files into this folder:
     * setup.bat
     * run_sender.bat
     * whatsapp_sender.py
     * contacts.csv
     * README.txt

STEP 3: Install Python (if not installed)
   - Double-click setup.bat
   - If Python is not installed, it will open download page
   - Download Python (latest version)
   - IMPORTANT: During installation, CHECK "Add Python to PATH"
   - After installation, run setup.bat again

STEP 4: Setup completes automatically
   - setup.bat will install required packages
   - Wait for "Installation Complete!" message


📝 PREPARE YOUR CONTACTS
-------------------------

STEP 5: Edit contacts.csv
   - Open contacts.csv in Excel or Notepad
   - Format: Name,Phone (with country code, no spaces)
   - Example:
     Name,Phone
     Sudhanshu Kumar,919876543210
     Naresh Prajapati,919876543211
   
   - Replace with your actual contacts
   - Save the file


📤 SENDING MESSAGES
-------------------

STEP 6: Customize your message (optional)
   - Open whatsapp_sender.py in Notepad
   - Find line: MESSAGE_TEMPLATE = "Hello {name}..."
   - Change the message text as needed
   - {name} will be replaced with actual names
   - Save the file

STEP 7: Run the sender
   - Double-click run_sender.bat
   - Chrome browser will open WhatsApp Web
   - SCAN QR CODE with your phone (you have 45 seconds)
   - Script will automatically send all messages!


⚙️ SETTINGS YOU CAN CHANGE
---------------------------

In whatsapp_sender.py, you can modify:

1. Message Template (Line 14):
   MESSAGE_TEMPLATE = "Your custom message here"

2. Delay between messages (Line 15):
   DELAY_BETWEEN_MESSAGES = 10  # Change to 5, 15, 20, etc.


❓ TROUBLESHOOTING
------------------

Problem: "Python is not installed"
Solution: Run setup.bat, it will help you install Python

Problem: "contacts.csv not found"
Solution: Make sure contacts.csv is in the same folder

Problem: Chrome doesn't open
Solution: Install Google Chrome browser

Problem: QR code doesn't appear
Solution: Wait a few more seconds, or check internet connection

Problem: Messages not sending
Solution: 
   - Check phone numbers have country code (91 for India)
   - Increase DELAY_BETWEEN_MESSAGES to 15-20 seconds
   - Make sure WhatsApp Web is working manually first


📞 PHONE NUMBER FORMAT
----------------------
✅ Correct: 919876543210 (country code + number, no spaces)
❌ Wrong: +91 9876543210
❌ Wrong: 9876543210 (missing country code)


⚠️ IMPORTANT NOTES
-------------------
1. Use only for people who have consented
2. Don't spam - WhatsApp may ban your number
3. Keep delay at least 10 seconds
4. Test with 2-3 contacts first
5. Keep browser window open until all messages sent


🎯 QUICK START SUMMARY
-----------------------
1. Create folder "WhatsApp_Sender"
2. Save all 5 files in it
3. Double-click setup.bat (installs Python + packages)
4. Edit contacts.csv with your contacts
5. Double-click run_sender.bat
6. Scan QR code
7. Wait for completion!


============================================================
Need help? Check the troubleshooting section above!
============================================================