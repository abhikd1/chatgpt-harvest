import re
import os

MASTER_FILE = "master_harvest.html"

if os.path.exists(MASTER_FILE):
    with open(MASTER_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 🧬 Surgical update for existing entries
    # We find each harvest-entry and its ID, then inject the copy button if not present
    def inject_copy(match):
        entry_id = match.group(1)
        controls_start = match.group(2)
        rest = match.group(3)
        
        if 'copyEntry' in controls_start or 'copyEntry' in rest:
            return match.group(0)
            
        copy_btn = f'\n                <button onclick="copyEntry(\'{entry_id}\')" class="control-btn copy-btn" title="Copy">📋</button>'
        return f'<div class="harvest-entry" id="{entry_id}"{controls_start}{copy_btn}{rest}'

    # Pattern: <div class="harvest-entry" id="ID" ...> <div class="entry-controls" ...>
    pattern = r'<div class="harvest-entry" id="([^"]+)"([^>]*>.*?<div class="entry-controls"[^>]*>)(.*?)'
    new_content = re.sub(pattern, inject_copy, content, flags=re.DOTALL)
    
    with open(MASTER_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully updated master_harvest.html with individual copy buttons.")
else:
    print("master_harvest.html not found, skipping update.")
