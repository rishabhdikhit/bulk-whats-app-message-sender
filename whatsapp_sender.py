# whatsapp_sender.py
# WhatsApp Bulk Message Sender using Selenium

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
import ctypes  # Required to prevent system sleep

# ============================================================
# CONFIGURATION
# ============================================================

MESSAGE_TEMPLATE = """Exciting Job Opportunity: Telesales Executive

Hi {name},

I found your profile on Job Hai. I have a vacancy for: 

Tele Sales Executive
Company - DUNNWOOD HEALTH PRIVATE LIMITED 
Salary - ₹20000 per month (in hand) + 15000 (Performance Based Incentive) 
Location - Uttam Nagar, Delhi 

If interested, please share your resume"""

# Short delay between individual messages
DELAY_MIN_SECONDS = 10
DELAY_MAX_SECONDS = 40

# --- SPAM PROTECTION CONFIGURATION ---
# Pause after sending this many messages (randomized range)
BATCH_SIZE_MIN = 15
BATCH_SIZE_MAX = 20

# How long to wait when batch limit is reached (in seconds)
# 300 sec = 5 mins, 600 sec = 10 mins
LONG_PAUSE_MIN_SECONDS = 300
LONG_PAUSE_MAX_SECONDS = 600

CONTACTS_FILE = "contacts.csv"

# ============================================================
# SYSTEM FUNCTIONS
# ============================================================

def prevent_sleep():
    """Prevents Windows from sleeping while script is running"""
    # ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000003)

def allow_sleep():
    """Allows Windows to sleep again"""
    # ES_CONTINUOUS
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)

def print_header():
    print("\n" + "=" * 70)
    print(" " * 15 + "WhatsApp Bulk Message Sender")
    print("=" * 70 + "\n")

def check_contacts_file():
    if not os.path.exists(CONTACTS_FILE):
        print(f"❌ ERROR: {CONTACTS_FILE} not found!")
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
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())
        except:
            if os.path.exists("chromedriver.exe"):
                service = Service("chromedriver.exe")
            else:
                service = Service()
        
        driver = webdriver.Chrome(service=service, options=options)
        print("✅ Chrome browser started successfully!\n")
        return driver
    except Exception as e:
        print(f"\n❌ ERROR: Could not start Chrome browser: {str(e)}\n")
        return None

def load_contacts():
    print(f"📂 Loading contacts from {CONTACTS_FILE}...")
    try:
        with open(CONTACTS_FILE, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            contacts = list(reader)
        if not contacts:
            print(f"❌ ERROR: No contacts found")
            return None
        print(f"✅ Loaded {len(contacts)} contacts\n")
        return contacts
    except Exception as e:
        print(f"❌ ERROR reading contacts file: {str(e)}")
        return None

def wait_for_whatsapp_login(driver):
    driver.get("https://web.whatsapp.com")
    print("=" * 70)
    print(" " * 20 + "⚡ SCAN QR CODE NOW! ⚡")
    print("=" * 70)
    print("\n  ⏰ Waiting 45 seconds for you to login...")
    time.sleep(45)
    print("✅ Proceeding to send messages...\n")

def send_message_to_contact(driver, contact, index, total):
    name = contact.get('Name', '').strip()
    phone = contact.get('Phone', '').strip()
    
    if not name or not phone:
        print(f"[{index}/{total}] ⚠️  Skipping - Missing name or phone")
        return False
    
    phone = ''.join(filter(str.isdigit, phone))
    message = MESSAGE_TEMPLATE.replace('{name}', name)
    
    print(f"[{index}/{total}] 📤 Sending to: {name} ({phone})")
    
    try:
        driver.get(f"https://web.whatsapp.com/send?phone={phone}")
        wait = WebDriverWait(driver, 40)
        
        message_box = None
        selectors = [
            '//div[@contenteditable="true"][@data-tab="10"]',
            '//div[@contenteditable="true"][@data-lexical-editor="true"]',
            '//div[@contenteditable="true"][@role="textbox"]'
        ]
        
        for selector in selectors:
            try:
                message_box = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
                break
            except:
                continue
        
        if not message_box:
            print(f"  ❌ Could not find message box")
            return False
        
        time.sleep(2)
        lines = message.split('\n')
        for i, line in enumerate(lines):
            message_box.send_keys(line)
            if i < len(lines) - 1:
                message_box.send_keys(Keys.SHIFT + Keys.ENTER)
        
        time.sleep(1)
        message_box.send_keys(Keys.ENTER)
        print(f"  ✅ Message sent successfully!")
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return False

def send_bulk_messages():
    print_header()
    if not check_contacts_file(): return
    driver = setup_driver()
    if not driver: return
    contacts = load_contacts()
    if not contacts: driver.quit(); return
    
    wait_for_whatsapp_login(driver)
    
    print("=" * 70)
    print(" " * 20 + "🚀 SENDING MESSAGES...")
    print("=" * 70 + "\n")
    
    successful = 0
    failed = 0
    
    # Logic for Spam Protection
    messages_in_current_batch = 0
    current_batch_limit = random.randint(BATCH_SIZE_MIN, BATCH_SIZE_MAX)
    
    prevent_sleep() # Prevent sleep while script is active
    
    for idx, contact in enumerate(contacts, 1):
        success = send_message_to_contact(driver, contact, idx, len(contacts))
        
        if success:
            successful += 1
            messages_in_current_batch += 1
        else:
            failed += 1
        
        # Check if we need a LONG PAUSE (Spam Protection)
        if messages_in_current_batch >= current_batch_limit and idx < len(contacts):
            wait_time = random.randint(LONG_PAUSE_MIN_SECONDS, LONG_PAUSE_MAX_SECONDS)
            wait_mins = round(wait_time / 60, 1)
            
            print("\n" + "!" * 60)
            print(f"🛡️  SPAM PROTECTION TRIGGERED")
            print(f"   Sent {messages_in_current_batch} messages. Pausing for {wait_mins} minutes...")
            print(f"   (Computer will remain awake)")
            print("!" * 60 + "\n")
            
            # Countdown timer
            remaining = wait_time
            while remaining > 0:
                print(f"   ⏳ Resuming in {remaining} seconds...", end='\r')
                time.sleep(1)
                remaining -= 1
                # Refresh anti-sleep every second just in case
                prevent_sleep()
            
            print("\n   ✅ Resuming sending now...\n")
            
            # Reset batch counters
            messages_in_current_batch = 0
            current_batch_limit = random.randint(BATCH_SIZE_MIN, BATCH_SIZE_MAX)
            
        # Standard short delay between messages
        elif idx < len(contacts):
            delay = random.randint(DELAY_MIN_SECONDS, DELAY_MAX_SECONDS)
            print(f"  ⏳ Waiting {delay} seconds...\n")
            time.sleep(delay)
    
    allow_sleep() # Allow sleep again
    
    print("\n" + "=" * 70)
    print(" " * 25 + "📊 SUMMARY")
    print("=" * 70)
    print(f"  Total contacts:  {len(contacts)}")
    print(f"  ✅ Successful:    {successful}")
    print(f"  ❌ Failed:        {failed}")
    print("=" * 70)
    
    if successful > 0:
        print("\n🎉 Messages sent successfully!")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    try:
        send_bulk_messages()
    except KeyboardInterrupt:
        print("\n\n⚠️  Stopped by user (Ctrl+C)")
        allow_sleep()
        input("\nPress Enter to exit...")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")
        allow_sleep()
        input("\nPress Enter to exit...")