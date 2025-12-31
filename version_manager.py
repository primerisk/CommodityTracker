import json
import datetime
import re
import os

VERSION_FILE = "version_info.json"
APP_FILE = "app.py"

def bump_version():
    today = datetime.date.today().isoformat()
    
    if not os.path.exists(VERSION_FILE):
        print(f"Error: {VERSION_FILE} not found.")
        return

    with open(VERSION_FILE, "r") as f:
        current_data = json.load(f)
            
    current_version = current_data.get("version", "1.0.0")
    # Clean version string (remove 'v' prefix if present in json, though we store without v usually)
    clean_version = current_version.replace('v', '')
    last_updated = current_data.get("last_updated", today)
    
    major, minor, patch = map(int, clean_version.split('.'))
    
    if today > last_updated:
        # New day: Increment Minor, Reset Patch
        print(f"New day detected ({today} > {last_updated}). Incrementing Minor.")
        minor += 1
        patch = 0
    else:
        # Same day: Increment Patch
        print("Same day. Incrementing Patch.")
        patch += 1
        
    new_version_str = f"{major}.{minor}.{patch}"
    new_data = {"version": new_version_str, "last_updated": today}
    
    # Write JSON
    with open(VERSION_FILE, "w") as f:
        json.dump(new_data, f, indent=4)
        
    # Update app.py
    if os.path.exists(APP_FILE):
        with open(APP_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Regex replace APP_VERSION = "vX.Y.Z"
        # We assume consistent formatting in app.py
        new_content = re.sub(
            r'APP_VERSION = "v\d+\.\d+\.\d+"', 
            f'APP_VERSION = "v{new_version_str}"', 
            content
        )
        
        with open(APP_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated {APP_FILE} to v{new_version_str}")
    else:
        print(f"Warning: {APP_FILE} not found. Skipped updating app source.")
        
    print(f"Version bumped from {current_version} to {new_version_str}")

if __name__ == "__main__":
    bump_version()
