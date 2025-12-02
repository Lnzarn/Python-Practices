import json
import re
import time
import random
import os
from typing import List
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pyperclip


class NovelTranslator:
    def __init__(self):
        """Initialize the translator with configuration"""
        # Set the correct folder path
        self.folder = r"C:\Users\User\OneDrive\Desktop\Coding\Python Practices\Advance Practices\Translator"
        self.load_config()

    def load_config(self):
        """Load configuration from JSON file"""
        config_path = os.path.join(self.folder, "config.json")

        if os.path.exists(config_path):
            print("Loaded: Config File.")
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            # Default configuration
            config = {
                "dictionary_path": "dictionary.json",
                "input_file": "input_novel.txt",
                "output_file": "translated_novel.txt",
                "deepl_wait_time": 20,
                "qwen_wait_time": 110,
                "deepl_chunk_size": 1450,
                "human_delay_min": 15,
                "human_delay_max": 33
            }
            # Save default config
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            print(f"Created default config file: {config_path}")

        self.config = config
        self.dictionary = self.load_dictionary()

    def load_dictionary(self):
        """Load translation dictionary"""
        dict_path = os.path.join(self.folder, self.config["dictionary_path"])

        if os.path.exists(dict_path):
            with open(dict_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Create empty dictionary template
            sample_dict = {
                "李明": "Li Ming",
                "玄天宗": "Xuantian Sect",
                "灵气": "Spiritual Qi"
            }
            with open(dict_path, 'w', encoding='utf-8') as f:
                json.dump(sample_dict, f, indent=2, ensure_ascii=False)
            print(f"Created sample dictionary: {dict_path}")
            return sample_dict

    def translate_chapter_titles(self, text):
        """Translate Chinese chapter titles to English format"""
        print("\n🔄 Translating chapter titles...")

        def replace_chapter(match):
            chapter_num = match.group(1)
            return f"Chapter {chapter_num} "

        modified_text = re.sub(r'第(\d+)章\s*', replace_chapter, text)

        new_count = len(re.findall(r'Chapter \d+', modified_text))
        print(f"✓ Translated {new_count} chapter titles (第X章 → Chapter X)")

        return modified_text

    def apply_dictionary(self, text):
        """Apply dictionary replacements to text"""
        print("\n=== Stage 1: Applying Dictionary ===")

        # First, translate chapter titles
        modified_text = self.translate_chapter_titles(text)

        # Then apply custom dictionary
        print("\n🔄 Applying custom dictionary...")
        replacements_made = 0

        for chinese, english in self.dictionary.items():
            if chinese in modified_text:
                count = modified_text.count(chinese)
                modified_text = modified_text.replace(chinese, english)
                replacements_made += count
                print(f"Replaced '{chinese}' → '{english}' ({count} times)")

        print(f"Total custom replacements: {replacements_made}")
        return modified_text

    def extract_chapters(self, text):
        """Extract chapters from text - supports 'Chapter X' format"""
        chapter_pattern = r'(Chapter\s+\d+.*?)(?=Chapter\s+\d+|$)'
        chapters = re.findall(chapter_pattern, text, re.DOTALL | re.IGNORECASE)

        if chapters:
            print(f"✓ Found {len(chapters)} chapters using pattern: Chapter X")
            return chapters

        print("⚠️  Warning: No chapter markers found. Treating as single chapter.")
        return [text]

    def get_chapter_number(self, chapter_text):
        """Extract chapter number from chapter text"""
        match = re.match(r'Chapter\s+(\d+)',
                         chapter_text.strip(), re.IGNORECASE)
        if match:
            return int(match.group(1))
        return None

    def setup_driver(self):
        """Setup Selenium WebDriver with stealth options"""
        from selenium.webdriver.chrome.service import Service

        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        chromedriver_path = os.path.join(
            self.folder, "chromedriver-win64", "chromedriver.exe")

        if os.path.exists(chromedriver_path):
            service = Service(chromedriver_path)
            driver = webdriver.Chrome(service=service, options=options)
        else:
            print(f"⚠️  ChromeDriver not found at: {chromedriver_path}")
            print("   Trying system PATH...")
            driver = webdriver.Chrome(options=options)

        driver.set_page_load_timeout(60)
        driver.implicitly_wait(10)

        return driver

    def split_text(self, text, max_size):
        """Split text into chunks of max_size"""
        chunks = []
        for i in range(0, len(text), max_size):
            chunks.append(text[i:i+max_size])
        return chunks

    def translate_with_deepl_web(self, text, driver):
        """Translate using DeepL website"""
        try:
            driver.get("https://www.deepl.com/translator")
        except:
            pass

        time.sleep(5)

        # Handle cookie banner
        try:
            cookie_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button[data-testid='cookie-banner-strict-accept-all']"))
            )
            cookie_btn.click()
            time.sleep(1)
        except:
            pass

        # Find source input
        source_textarea = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[contenteditable='true']"))
        )

        source_textarea.click()
        time.sleep(1)
        source_textarea.clear()
        time.sleep(0.5)

        pyperclip.copy(text)
        source_textarea.send_keys(Keys.CONTROL, 'v')

        wait_time = self.config["deepl_wait_time"]
        print(f"   Waiting {wait_time}s for translation...")
        time.sleep(wait_time)

        target_textarea = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "d-textarea[data-testid='translator-target-input']"))
        )
        translated = target_textarea.get_attribute('value')

        if not translated:
            raise Exception("Could not get translation from DeepL")

        print(f"   📝 DeepL output preview: {translated[:100]}...")
        return translated

    def translate_with_qwen_web(self, text, driver):
        """Translate using Qwen website"""
        driver.get("https://chat.qwen.ai/")
        time.sleep(5)

        # Find input field
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea"))
        )

        prompt = f"Translate the following Chinese novel text to English. Maintain narrative style and cultural context. Only output the translation:\n\n{text}"

        input_field.click()
        time.sleep(1)
        pyperclip.copy(prompt)
        input_field.send_keys(Keys.CONTROL, 'v')
        time.sleep(1)
        input_field.send_keys(Keys.RETURN)

        wait_time = self.config["qwen_wait_time"]
        print(f"   Waiting {wait_time}s for Qwen to finish responding...")
        time.sleep(wait_time)

        # Use the working selector from test
        print("   🔍 Getting Qwen response...")
        try:
            response_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#response-message-body > div.text-response-render-container"))
            )
            translated = response_element.text

            if not translated or len(translated) < 20:
                raise Exception("Response too short or empty")

            print(f"   📝 Qwen output preview: {translated[:100]}...")
            return translated

        except Exception as e:
            print(f"   ⚠️  Primary selector failed: {e}")
            print("   Trying fallback selectors...")

            # Fallback selectors
            fallback_selectors = [
                "div[class*='text-response-render-container']",
                "div[class*='message']"
            ]

            for selector in fallback_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        translated = elements[-1].text
                        if translated and len(translated) > 20:
                            print(f"   ✓ Used fallback: {selector}")
                            print(
                                f"   📝 Qwen output preview: {translated[:100]}...")
                            return translated
                except:
                    continue

            raise Exception(
                "Could not get response from Qwen with any selector")

    def translate_with_web(self, chapters, output_file, website):
        """Translate chapters using web automation"""
        print(f"\n=== Translating with {website.upper()} Website ===")

        driver = self.setup_driver()
        last_chinese_text = ""

        # Get chunk size for this website
        chunk_size = self.config["deepl_chunk_size"] if website == "deepl" else None

        try:
            for i, chapter in enumerate(chapters):
                chapter_num = self.get_chapter_number(chapter)
                chapter_display = f"Chapter {chapter_num}" if chapter_num else f"Section {i+1}"

                print(
                    f"\n📖 Translating: {chapter_display} ({i+1}/{len(chapters)})")
                print(f"   Chapter size: {len(chapter)} characters")

                # Only DeepL needs splitting - Qwen handles full chapters
                if website == "deepl" and len(chapter) > chunk_size:
                    print(f"   Chapter too large for DeepL, splitting into parts...")
                    parts = self.split_text(chapter, chunk_size)

                    for part_idx, part in enumerate(parts, 1):
                        print(
                            f"   Translating {chapter_display} - Part {part_idx}/{len(parts)}...")
                        try:
                            translated = self.translate_with_deepl_web(
                                part, driver)

                            # Append to file immediately
                            with open(output_file, 'a', encoding='utf-8') as f:
                                f.write(translated + "\n\n")

                            print(f"   ✓ Part {part_idx} translated and saved")
                            last_chinese_text = part[-200:]
                            time.sleep(3)

                        except Exception as e:
                            print(f"   ✗ Error on Part {part_idx}: {e}")
                            print(f"\n❌ CRASH DETECTED!")
                            print(
                                f"Last successfully translated text (last 200 chars):")
                            print(f"'{last_chinese_text}'")
                            raise
                else:
                    # Translate full chapter (for Qwen or small DeepL chapters)
                    try:
                        if website == "deepl":
                            translated = self.translate_with_deepl_web(
                                chapter, driver)
                        else:  # qwen - always full chapter
                            print(f"   Translating full chapter with Qwen...")
                            translated = self.translate_with_qwen_web(
                                chapter, driver)

                        # Append to file immediately
                        with open(output_file, 'a', encoding='utf-8') as f:
                            f.write(translated + "\n\n")

                        print(f"   ✓ Full chapter translated and saved")
                        last_chinese_text = chapter[-200:]
                        time.sleep(5)

                    except Exception as e:
                        print(f"   ✗ Error: {e}")
                        print(f"\n❌ CRASH DETECTED!")
                        print(f"Last successfully translated text (last 200 chars):")
                        print(f"'{last_chinese_text}'")
                        raise

        finally:
            driver.quit()

    def translate_novel(self):
        """Main translation pipeline"""
        print("=" * 60)
        print("📚 NOVEL TRANSLATION PIPELINE")
        print("=" * 60)

        # Load input file
        input_file = os.path.join(self.folder, self.config["input_file"])

        if not os.path.exists(input_file):
            print(f"Error: Input file not found: {input_file}")
            return

        with open(input_file, 'r', encoding='utf-8') as f:
            original_text = f.read()

        print(
            f"Loaded: {self.config['input_file']} ({len(original_text)} characters)")

        # Stage 1: Apply dictionary
        processed_text = self.apply_dictionary(original_text)

        # Save to temp file
        temp_file = os.path.join(self.folder, "temp_dictionary_applied.txt")
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(processed_text)

        print(f"\n✓ Dictionary applied. Saved to: {temp_file}")
        print("Please review the temp file to verify dictionary replacements.")

        while True:
            confirm = input(
                "\nContinue with this text? (yes/no/exit): ").strip().lower()
            if confirm == "yes":
                os.remove(temp_file)
                print("✓ Temp file deleted. Continuing...")
                break
            elif confirm == "no":
                print("\n♻️  Reapplying dictionary...")
                processed_text = self.apply_dictionary(original_text)
                with open(temp_file, 'w', encoding='utf-8') as f:
                    f.write(processed_text)
                print(f"✓ Reapplied. Saved to: {temp_file}")
            elif confirm == "exit":
                print("Exiting...")
                return
            else:
                print("Invalid input. Please type 'yes', 'no', or 'exit'.")

        # Extract chapters
        chapters = self.extract_chapters(processed_text)
        print(f"\nFound {len(chapters)} chapters")

        # Ask user for translation method
        while True:
            print("\n" + "=" * 60)
            print("Choose translation method:")
            print("1. DeepL Website (Best quality, splits large chapters)")
            print("2. Qwen Website (AI-powered, translates FULL chapters)")
            print("3. Exit")
            print("=" * 60)

            choice = input("Enter choice (1-3): ").strip()

            if choice == "3":
                print("Exiting...")
                return

            if choice not in ["1", "2"]:
                print("Invalid choice. Please enter 1, 2, or 3.")
                continue

            # Clear output file before starting
            output_file = os.path.join(self.folder, self.config["output_file"])
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("")  # Clear file

            try:
                if choice == "1":
                    self.translate_with_web(chapters, output_file, "deepl")
                elif choice == "2":
                    self.translate_with_web(chapters, output_file, "qwen")

                print("\n" + "=" * 60)
                print("✅ TRANSLATION COMPLETE!")
                print(f"Output saved to: {output_file}")
                print("=" * 60)
                return

            except Exception as e:
                print(f"\n❌ Translation failed: {e}")
                print(f"Partial translation saved to: {output_file}")

                retry = input(
                    "\nDo you want to try again with a different method? (yes/no): ").strip().lower()
                if retry != "yes":
                    print("Exiting...")
                    return


def main():
    print("Novel Translation Automation System")
    print("DeepL Web | Qwen Web")
    print("=" * 60)

    translator = NovelTranslator()
    translator.translate_novel()


if __name__ == "__main__":
    main()
