# whatsapp_sender.py
# WhatsApp Bulk Message Sender using Selenium
# Created for automated WhatsApp messaging via WhatsApp Web

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import csv
import os
import random

# ============================================================
# CONFIGURATION - EDIT THESE SETTINGS
# ============================================================

# Your message template - use {name} where you want the person's name
MESSAGE_TEMPLATE = """Hi {name}, I'm Rishabh from Dunnwood Health. We are currently hiring for the role of Customer Excellence Executive in Bengaluru and came across your profile on Apna. Could you please let me know a convenient time for a quick call to discuss this opportunity?"""

# Delay between messages in seconds (will be random between MIN and MAX)
DELAY_MIN_SECONDS = 3
DELAY_MAX_SECONDS = 10

# Name of your contacts file
CONTACTS_FILE = "contacts.csv"

# ============================================================
# MAIN PROGRAM - DO NOT EDIT BELOW THIS LINE
# ============================================================

def print_header():
    print("\n" + "=" * 70)
    print(" " * 15 + "WhatsApp Bulk Message Sender")
    print("=" * 70 + "\n")

def check_contacts_file():
    if not os.path.exists(CONTACTS_FILE):
        print(f"❌ ERROR: {CONTACTS_FILE} not found!")
        print(f"\nPlease create {CONTACTS_FILE} with the following format:")
        print("-" * 50)
        print("Name,Phone")
        print("Sudhanshu Kumar,919876543210")
        print("Naresh Prajapati,919876543211")
        print("-" * 50)
        input("\nPress Enter to exit...")
        return False
    return True

def setup_driver():
    print("🔧 Setting up Chrome browser...")
    
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("detach", True)
    
    try:
        # Try to use webdriver-manager
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())
        except:
            # Fallback to local chromedriver
            if os.path.exists("chromedriver.exe"):
                service = Service("chromedriver.exe")
            else:
                service = Service()
        
        driver = webdriver.Chrome(service=service, options=options)
        print("✅ Chrome browser started successfully!\n")
        return driver
        
    except Exception as e:
        print(f"\n❌ ERROR: Could not start Chrome browser")
        print(f"Details: {str(e)}\n")
        print("Please ensure:")
        print("  1. Google Chrome is installed")
        print("  2. Run setup.bat to install required packages")
        input("\nPress Enter to exit...")
        return None

def load_contacts():
    print(f"📂 Loading contacts from {CONTACTS_FILE}...")
    
    contacts = []
    try:
        with open(CONTACTS_FILE, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            contacts = list(reader)
        
        if not contacts:
            print(f"❌ ERROR: No contacts found in {CONTACTS_FILE}")
            return None
            
        print(f"✅ Loaded {len(contacts)} contacts\n")
        return contacts
        
    except Exception as e:
        print(f"❌ ERROR reading contacts file: {str(e)}")
        input("\nPress Enter to exit...")
        return None

def wait_for_whatsapp_login(driver):
    driver.get("https://web.whatsapp.com")
    
    print("=" * 70)
    print(" " * 20 + "⚡ SCAN QR CODE NOW! ⚡")
    print("=" * 70)
    print("\n  1. Open WhatsApp on your phone")
    print("  2. Go to Settings > Linked Devices")
    print("  3. Tap 'Link a Device'")
    print("  4. Scan the QR code on screen")
    print("\n  ⏰ Waiting 45 seconds for you to login...")
    print("\n" + "=" * 70 + "\n")
    
    time.sleep(45)
    print("✅ Proceeding to send messages...\n")

def send_message_to_contact(driver, contact, index, total):
    name = contact.get('Name', '').strip()
    phone = contact.get('Phone', '').strip()
    
    if not name or not phone:
        print(f"[{index}/{total}] ⚠️  Skipping - Missing name or phone")
        return False
    
    # Clean phone number
    phone = ''.join(filter(str.isdigit, phone))
    
    # Personalize message
    message = MESSAGE_TEMPLATE.replace('{name}', name)
    
    print(f"[{index}/{total}] 📤 Sending to: {name} ({phone})")
    
    try:
        # Navigate to chat
        driver.get(f"https://web.whatsapp.com/send?phone={phone}")
        
        # Wait for message box with extended timeout
        wait = WebDriverWait(driver, 40)
        
        # Try multiple selectors for message box
        message_box = None
        selectors = [
            '//div[@contenteditable="true"][@data-tab="10"]',
            '//div[@contenteditable="true"][@data-lexical-editor="true"]',
            '//div[@contenteditable="true"][@role="textbox"]'
        ]
        
        for selector in selectors:
            try:
                message_box = wait.until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                break
            except:
                continue
        
        if not message_box:
            print(f"  ❌ Could not find message box")
            return False
        
        # Small delay to ensure box is ready
        time.sleep(2)
        
        # Type message line by line
        lines = message.split('\n')
        for i, line in enumerate(lines):
            message_box.send_keys(line)
            if i < len(lines) - 1:
                message_box.send_keys(Keys.SHIFT + Keys.ENTER)
        
        time.sleep(1)
        
        # Send message
        message_box.send_keys(Keys.ENTER)
        
        print(f"  ✅ Message sent successfully!")
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return False

def send_bulk_messages():
    print_header()
    
    # Check if contacts file exists
    if not check_contacts_file():
        return
    
    # Setup Chrome driver
    driver = setup_driver()
    if not driver:
        return
    
    # Load contacts
    contacts = load_contacts()
    if not contacts:
        driver.quit()
        return
    
    # Wait for WhatsApp login
    wait_for_whatsapp_login(driver)
    
    # Send messages
    print("=" * 70)
    print(" " * 20 + "🚀 SENDING MESSAGES...")
    print("=" * 70 + "\n")
    
    successful = 0
    failed = 0
    
    for idx, contact in enumerate(contacts, 1):
        success = send_message_to_contact(driver, contact, idx, len(contacts))
        
        if success:
            successful += 1
        else:
            failed += 1
        
        # Wait before next message (random delay)
        if idx < len(contacts):
            delay = random.randint(DELAY_MIN_SECONDS, DELAY_MAX_SECONDS)
            print(f"  ⏳ Waiting {delay} seconds...\n")
            time.sleep(delay)
    
    # Print summary
    print("\n" + "=" * 70)
    print(" " * 25 + "📊 SUMMARY")
    print("=" * 70)
    print(f"  Total contacts:  {len(contacts)}")
    print(f"  ✅ Successful:    {successful}")
    print(f"  ❌ Failed:        {failed}")
    print("=" * 70)
    
    if successful > 0:
        print("\n🎉 Messages sent successfully!")
    
    print("\n💡 Browser will remain open. Close it manually when done.")
    input("\nPress Enter to exit...")

# ============================================================
# RUN THE PROGRAM
# ============================================================

if __name__ == "__main__":
    try:
        send_bulk_messages()
    except KeyboardInterrupt:
        print("\n\n⚠️  Stopped by user (Ctrl+C)")
        input("\nPress Enter to exit...")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")
        input("\nPress Enter to exit...")