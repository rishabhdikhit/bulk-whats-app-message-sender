# extract_replied.py
# Extract phone numbers of people who replied (have unread messages)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import csv
import os
import re
from datetime import datetime

# ============================================================
# CONFIGURATION
# ============================================================

# Output CSV file name
OUTPUT_FILE = f"replied_contacts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

# Time to wait for WhatsApp Web to load (seconds)
LOAD_WAIT_TIME = 60

# ============================================================
# MAIN PROGRAM
# ============================================================

def print_header():
    print("\n" + "=" * 70)
    print(" " * 15 + "WhatsApp Replied Contacts Extractor")
    print("=" * 70 + "\n")

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
        print(f"\n❌ ERROR: Could not start Chrome browser")
        print(f"Details: {str(e)}\n")
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
    print(f"\n  ⏰ Waiting {LOAD_WAIT_TIME} seconds for you to login and chats to load...")
    print("\n" + "=" * 70 + "\n")
    
    time.sleep(LOAD_WAIT_TIME)
    print("✅ Proceeding to extract contacts...\n")

def extract_phone_from_text(text):
    """Extract phone number from text"""
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', text)
    
    # If it starts with country code, return it
    if len(digits) >= 10:
        return digits
    
    return None

def get_contact_info(driver, chat_element):
    """Get contact name and phone from a chat element"""
    try:
        # Click on the chat to open it
        chat_element.click()
        time.sleep(2)
        
        # Try to get contact name from header
        name = "Unknown"
        phone = None
        
        try:
            # Get name from chat header
            name_element = driver.find_element(By.XPATH, '//header//span[@dir="auto"]')
            name = name_element.text.strip()
        except:
            pass
        
        # Click on header to open contact info
        try:
            header = driver.find_element(By.XPATH, '//header')
            header.click()
            time.sleep(2)
            
            # Try to find phone number in contact info
            try:
                # Look for phone number in contact info
                phone_elements = driver.find_elements(By.XPATH, '//*[contains(text(), "+") or contains(text(), "91")]')
                for elem in phone_elements:
                    text = elem.text.strip()
                    extracted = extract_phone_from_text(text)
                    if extracted and len(extracted) >= 10:
                        phone = extracted
                        break
            except:
                pass
            
            # Close contact info
            try:
                close_btn = driver.find_element(By.XPATH, '//button[@aria-label="Close"]')
                close_btn.click()
                time.sleep(1)
            except:
                driver.find_element(By.TAG_NAME, 'body').click()
                time.sleep(1)
                
        except:
            pass
        
        # If we couldn't get phone, try to extract from chat title
        if not phone:
            try:
                # Check if name itself contains phone number
                phone = extract_phone_from_text(name)
            except:
                pass
        
        return name, phone
        
    except Exception as e:
        print(f"  ⚠️ Error extracting contact info: {str(e)}")
        return None, None

def extract_replied_contacts():
    print_header()
    
    # Setup Chrome driver
    driver = setup_driver()
    if not driver:
        return
    
    # Wait for WhatsApp login
    wait_for_whatsapp_login(driver)
    
    print("=" * 70)
    print(" " * 15 + "🔍 SEARCHING FOR UNREAD MESSAGES...")
    print("=" * 70 + "\n")
    
    replied_contacts = []
    
    try:
        # Scroll to load all chats
        print("📜 Loading all chats...")
        
        # Find the chat list container and scroll
        try:
            chat_list = driver.find_element(By.XPATH, '//div[@id="pane-side"]')
            for i in range(5):  # Scroll 5 times to load more chats
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", chat_list)
                time.sleep(1)
        except:
            pass
        
        print("✅ Chats loaded\n")
        
        # Find all chats with unread messages
        # Look for chats with unread badge/indicator
        unread_selectors = [
            '//div[contains(@class, "unread")]//ancestor::div[@role="listitem"]',
            '//span[@data-icon="unread-count"]//ancestor::div[@role="listitem"]',
            '//div[contains(@aria-label, "unread")]',
            '//span[contains(@class, "unread")]//ancestor::div[@role="listitem"]'
        ]
        
        unread_chats = []
        for selector in unread_selectors:
            try:
                chats = driver.find_elements(By.XPATH, selector)
                unread_chats.extend(chats)
            except:
                continue
        
        # Remove duplicates
        unread_chats = list(set(unread_chats))
        
        print(f"📬 Found {len(unread_chats)} chats with unread messages\n")
        
        if len(unread_chats) == 0:
            print("⚠️  No unread messages found!")
            print("Make sure you haven't opened the messages yet.\n")
        else:
            print("Extracting contact information...\n")
            
            for idx, chat in enumerate(unread_chats, 1):
                print(f"[{idx}/{len(unread_chats)}] Processing...")
                
                try:
                    # Get contact name and phone
                    name, phone = get_contact_info(driver, chat)
                    
                    if name and phone:
                        replied_contacts.append({
                            'Name': name,
                            'Phone': phone
                        })
                        print(f"  ✅ {name} - {phone}")
                    elif name:
                        replied_contacts.append({
                            'Name': name,
                            'Phone': 'Not found'
                        })
                        print(f"  ⚠️  {name} - Phone not found")
                    
                    # Go back to chat list
                    try:
                        back_btn = driver.find_element(By.XPATH, '//button[@aria-label="Back"]')
                        back_btn.click()
                        time.sleep(1)
                    except:
                        pass
                    
                except Exception as e:
                    print(f"  ❌ Error: {str(e)}")
                    continue
        
        # Save to CSV
        if replied_contacts:
            print(f"\n💾 Saving {len(replied_contacts)} contacts to {OUTPUT_FILE}...")
            
            with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['Name', 'Phone'])
                writer.writeheader()
                writer.writerows(replied_contacts)
            
            print(f"✅ Saved successfully!\n")
        
        # Print summary
        print("\n" + "=" * 70)
        print(" " * 25 + "📊 SUMMARY")
        print("=" * 70)
        print(f"  Total unread chats:     {len(unread_chats)}")
        print(f"  Contacts extracted:     {len(replied_contacts)}")
        print(f"  Output file:            {OUTPUT_FILE}")
        print("=" * 70)
        
        if replied_contacts:
            print("\n🎉 Contacts extracted successfully!")
            print(f"📁 Check the file: {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"\n❌ Error during extraction: {str(e)}")
    
    print("\n💡 Browser will remain open. Close it manually when done.")
    input("\nPress Enter to exit...")

# ============================================================
# RUN THE PROGRAM
# ============================================================

if __name__ == "__main__":
    try:
        extract_replied_contacts()
    except KeyboardInterrupt:
        print("\n\n⚠️  Stopped by user (Ctrl+C)")
        input("\nPress Enter to exit...")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")
        input("\nPress Enter to exit...")