# test_selectors.py - Test Qwen and Lara
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import os
import pyperclip


def setup_driver():
    """Setup Chrome with correct path"""
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # Set ChromeDriver path
    folder = r"C:\Users\User\OneDrive\Desktop\Coding\Python Practices\Advance Practices\Translator"
    chromedriver_path = os.path.join(
        folder, "chromedriver-win64", "chromedriver.exe")

    print(f"Looking for ChromeDriver at: {chromedriver_path}")

    if os.path.exists(chromedriver_path):
        print("✅ ChromeDriver found!")
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=options)
    else:
        print("❌ ChromeDriver not found in chromedriver-win64 folder")
        print("   Trying system PATH...")
        driver = webdriver.Chrome(options=options)

    driver.set_page_load_timeout(60)
    return driver


def test_qwen():
    """Test Qwen selectors with actual translation"""
    print("\n" + "="*60)
    print("🧪 Testing QWEN")
    print("="*60)

    driver = setup_driver()

    try:
        url = "https://chat.qwen.ai/"
        print(f"\n📍 Loading: {url}")
        driver.get(url)
        time.sleep(15)

        print(f"   Page title: {driver.title}")
        print(f"   Current URL: {driver.current_url}")

        # Check if login required
        if "login" in driver.current_url.lower():
            print("   ⚠️  Login page detected")
            input("\n   Press Enter to close...")
            return

        print("   ✅ Page loaded successfully")

        print("\n🔍 Looking for input field...")

        # Try common selectors for input
        input_selectors = [
            "textarea",
            "textarea.input",
            "div[contenteditable='true']",
            "textarea[placeholder]",
            "#input",
            ".chat-input",
            "textarea[role='textbox']"
        ]

        input_found = None
        input_element = None
        for selector in input_selectors:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                if element.is_displayed():
                    print(f"   ✅ FOUND INPUT: {selector}")
                    input_found = selector
                    input_element = element
                    break
            except:
                pass

        if not input_found:
            print("   ❌ No input field found")
            input("\n   Press Enter to close...")
            return

        # Now actually send a message
        print("\n📤 Sending test message...")
        test_text = "你好世界"

        input_element.click()
        time.sleep(1)
        pyperclip.copy(test_text)
        input_element.send_keys(Keys.CONTROL, 'v')
        time.sleep(1)
        input_element.send_keys(Keys.RETURN)

        print(f"   ✓ Sent: {test_text}")

        # Wait for response
        print("\n⏳ Waiting 30 seconds for Qwen to respond...")
        time.sleep(30)

        print("\n🔍 Looking for response area...")

        # Try response selectors in order
        response_selectors = [
            "#response-message-body > div.text-response-render-container",
            "div[class*='text-response-render-container']",
            "div[class*='message']",
            "div[class*='Message']",
            ".message-content",
            "div[class*='content']",
            "div[data-message-role='assistant']",
            ".markdown-body"
        ]

        response_found = None
        response_text = None

        for selector in response_selectors:
            try:
                print(f"   Trying: {selector}")
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    # Get the last element (most recent)
                    last_element = elements[-1]
                    text = last_element.text

                    if text and len(text) > 5:
                        print(f"   ✅ FOUND RESPONSE: {selector}")
                        print(f"   📝 Elements found: {len(elements)}")
                        print(f"   📝 Text length: {len(text)} chars")
                        print(f"   📝 Preview: {text[:200]}...")
                        response_found = selector
                        response_text = text
                        break
            except Exception as e:
                print(f"   ❌ Error with {selector}: {e}")
                continue

        if not response_found:
            print("\n   ⚠️  No response found with tested selectors")
            print("   💡 Trying to get all body text as fallback...")
            try:
                body = driver.find_element(By.TAG_NAME, "body")
                all_text = body.text
                print(f"   📝 Full page text preview:\n{all_text[:500]}...")
            except:
                pass

        print("\n" + "="*60)
        print("📝 QWEN TEST SUMMARY:")
        print(f"   Input selector: {input_found}")
        print(f"   Response selector: {response_found}")
        if response_text:
            print(f"   ✅ Successfully captured response!")
        else:
            print(f"   ❌ Could not capture response")
        print("="*60)

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

    finally:
        input("\n⏸  Press Enter to close Qwen test...")
        driver.quit()


def test_lara():
    """Test Lara selectors"""
    print("\n" + "="*60)
    print("🧪 Testing LARA")
    print("="*60)

    driver = setup_driver()

    try:
        url = "https://laratranslate.com/translate"
        print(f"\n📍 Loading: {url}")
        driver.get(url)
        time.sleep(15)

        print(f"   Page title: {driver.title}")
        print(f"   Current URL: {driver.current_url}")
        print("   ✅ Page loaded successfully")

        print("\n🔍 Looking for source input field...")

        # Try source input selectors
        source_selectors = [
            "#source-editable",
            "div[id*='source-editable']",
            "textarea#sourceText",
            "textarea[placeholder*='Enter']",
            "textarea[placeholder*='text']",
            "textarea[id*='source']",
            "textarea.source",
            "textarea",
            "div[contenteditable='true']"
        ]

        source_found = None
        source_element = None
        for selector in source_selectors:
            try:
                print(f"   Trying: {selector}")
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    element = elements[0]
                    if element.is_displayed():
                        print(f"   ✅ FOUND SOURCE INPUT: {selector}")
                        source_found = selector
                        source_element = element
                        break
            except Exception as e:
                print(f"   ❌ {selector}: {e}")
                continue

        if not source_found:
            print("   ❌ No source input found")
            print("\n   📸 Taking screenshot...")
            driver.save_screenshot("lara_no_input.png")
            print("   Saved: lara_no_input.png")
            input("\n   Press Enter to close...")
            return

        # Send test text
        print("\n📤 Sending test text...")
        test_text = "你好世界，这是一个测试。"

        source_element.click()
        time.sleep(1)
        pyperclip.copy(test_text)
        source_element.send_keys(Keys.CONTROL, 'v')
        print(f"   ✓ Pasted: {test_text}")

        # Wait for translation
        print("\n⏳ Waiting 20 seconds for translation...")
        time.sleep(20)

        print("\n🔍 Looking for translation output...")

        # Try output selectors
        target_selectors = [
            "div[id*='translatedText']",
            "textarea[id*='translated']",
            "textarea#targetText",
            "div[id*='target']",
            "textarea[id*='target']",
            "textarea[placeholder*='Translation']",
            "textarea.target",
            "div.translation-output",
            "div[class*='output']",
            "div[class*='translation']"
        ]

        target_found = None
        translation_text = None

        for selector in target_selectors:
            try:
                print(f"   Trying: {selector}")
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    element = elements[0]
                    text = element.get_attribute(
                        'value') or element.text or element.get_attribute('innerText')

                    if text and len(text) > 3:
                        print(f"   ✅ FOUND OUTPUT: {selector}")
                        print(f"   📝 Text length: {len(text)} chars")
                        print(f"   📝 Translation: {text[:200]}...")
                        target_found = selector
                        translation_text = text
                        break
            except Exception as e:
                print(f"   ❌ {selector}: {e}")
                continue

        if not target_found:
            print("\n   ⚠️  No translation found with tested selectors")
            print("   💡 Let me check all textareas on the page...")
            try:
                all_textareas = driver.find_elements(By.TAG_NAME, "textarea")
                print(f"   Found {len(all_textareas)} textareas total")
                for i, ta in enumerate(all_textareas):
                    value = ta.get_attribute('value') or ta.text
                    if value:
                        print(f"   Textarea {i}: {value[:100]}...")
            except:
                pass

        print("\n" + "="*60)
        print("📝 LARA TEST SUMMARY:")
        print(f"   Source selector: {source_found}")
        print(f"   Target selector: {target_found}")
        if translation_text:
            print(f"   ✅ Successfully captured translation!")
        else:
            print(f"   ❌ Could not capture translation")
        print("="*60)

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

    finally:
        input("\n⏸  Press Enter to close Lara test...")
        driver.quit()


def main():
    print("="*60)
    print("🔧 CSS SELECTOR TESTING TOOL")
    print("   Testing Qwen & Lara Translators")
    print("="*60)
    print("\nWhat would you like to test?")
    print("1. Qwen (https://chat.qwen.ai/)")
    print("2. Lara (https://laratranslate.com/translate)")
    print("3. Both")

    choice = input("\nEnter your choice (1-3): ").strip()

    if choice == "1":
        test_qwen()
    elif choice == "2":
        test_lara()
    elif choice == "3":
        test_qwen()
        test_lara()
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()
