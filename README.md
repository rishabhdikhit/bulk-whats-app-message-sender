"""
WhatsApp Automation Toolkit: Bulk Sender & Reply Extractor
This script-style documentation explains how to use the tools provided in this project.
"""

# -----------------------------------------
# 📂 Project Structure
# -----------------------------------------

project_files = [
    "setup.bat",              # Installs Python + needed libraries
    "run_batch.bat",          # Runs Bulk Message Sender
    "run_extract_batch.bat",  # Runs Reply Extractor
    "whatsapp_sender.py",     # Sends messages
    "extract_replied.py",     # Extracts unread replies
    "contacts.csv"            # Input contact list
]

# -----------------------------------------
# 🚀 Installation & Setup
# -----------------------------------------

###install_and_setup():
    """
    1. Download all project files into a folder, e.g., WhatsApp_Sender.
    2. Run setup.bat:
        - If Python is missing → Opens download page.
        - If Python exists → Installs selenium and webdriver-manager.
    3. Wait for "Installation Complete!".
    """
    pass


# -----------------------------------------
# 📨 Module 1: Bulk Message Sender
# -----------------------------------------

# Example format inside contacts.csv
contacts_csv_format = """
Name,Phone
Sudhanshu Kumar,919876543210
Naresh Prajapati,919876543211
"""

# Message Template Example
MESSAGE_TEMPLATE = "Hello {name}, this is a sample WhatsApp message."

# Delay settings
DELAY_MIN_SECONDS = 10
DELAY_MAX_SECONDS = 20

### run_bulk_sender():
    """
    Steps:
        1. Double-click run_batch.bat.
        2. Chrome opens WhatsApp Web.
        3. Scan QR code within 45 seconds.
        4. Script sends messages to all contacts in contacts.csv.
    """
    pass


# -----------------------------------------
# 📥 Module 2: Reply Extractor
# -----------------------------------------

### run_reply_extractor():
    """
    Prerequisite:
        - Do NOT open any messages before running.
        - Script identifies chats with unread indicators.

    Steps:
        1. Double-click run_extract_batch.bat.
        2. Scan QR code if asked (timeout = 60 seconds).
        3. Script scrolls and finds unread chats.
        4. Creates file: replied_contacts_YYYYMMDD_HHMMSS.csv
    """
    pass


# -----------------------------------------
# ❓ Troubleshooting
# -----------------------------------------

### troubleshooting():
    issues = {
        "PythonNotInstalled": "Run setup.bat or manually install Python 3.x (check Add to PATH).",
        "ContactsFileMissing": "Ensure contacts.csv is inside the folder.",
        "MessagesNotSending": [
            "Ensure phone numbers include country code (e.g., 9198...).",
            "No spaces or '+' allowed.",
            "Increase delay settings in script."
        ],
        "QRCodeNotVisible": "Wait some seconds or check internet connection."
    }
    return issues


# -----------------------------------------
# ⚠️ Disclaimer & Best Practices
# -----------------------------------------

BEST_PRACTICES = [
    "Use this tool only with user consent.",
    "Avoid spamming; WhatsApp may block your number.",
    "Keep message delay to at least 10 seconds."
]


# If this script were executable:
if __name__ == "__main__":
    print("WhatsApp Automation Toolkit Documentation Loaded")
