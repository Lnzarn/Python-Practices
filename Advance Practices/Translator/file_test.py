import os
import json

print("="*60)
print("🔍 FILE DIAGNOSTIC TOOL")
print("="*60)

# Check current working directory
print(f"\n📁 Current working directory:")
print(f"   {os.getcwd()}")

# List all files in current directory
print(f"\n📂 Files in current directory:")
folder = r"C:\Users\User\OneDrive\Desktop\Coding\Python Practices\Advance Practices\Translator"

print(f"\n📂 Files in target directory:")
files = os.listdir(folder)

for f in sorted(files):
    full = os.path.join(folder, f)

    if os.path.isfile(full):
        size = os.path.getsize(full)
        print(f"   ✓ {f} ({size:,} bytes)")
    elif os.path.isdir(full):
        print(f"   📁 {f}/")


# Check specifically for input_novel.txt
target_file = os.path.join(folder, "input_novel.txt")

print(f"\n🔎 Looking for 'input_novel.txt':")
if os.path.exists(target_file):
    print(f"   ✅ FOUND!")
    size = os.path.getsize(target_file)
    print(f"   Size: {size:,} bytes")

    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            preview = f.read(100)
            print(f"   Preview: {preview[:100]}...")
    except Exception as e:
        print(f"   ⚠️  Error reading file: {e}")
else:
    print(f"   ❌ NOT FOUND (checked path: {target_file})")


# Check config.json
print(f"\n⚙️  Checking config.json:")
if os.path.exists('config.json'):
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            print(f"   input_file setting: '{config.get('input_file')}'")
    except Exception as e:
        print(f"   ⚠️  Error reading config: {e}")
else:
    print(f"   ❌ config.json not found")

print("\n" + "="*60)
print("💡 TIPS:")
print("   • Make sure the file is named exactly: input_novel.txt")
print("   • Check for extra spaces in the filename")
print("   • Make sure it's a .txt file (not .txt.txt)")
print("   • File should be in the same folder as Translator.py")
print("="*60)
