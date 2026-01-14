import re
import os

MASTER_FILE = "master_harvest.html"

if os.path.exists(MASTER_FILE):
    with open(MASTER_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    def migrate_entry(match):
        entry_id = match.group(1)
        entry_style = match.group(2)
        controls_style = match.group(3)
        controls_inner = match.group(4)
        
        # 1. Ensure align-items: center in controls
        if 'align-items: center' not in controls_style:
            controls_style = controls_style.replace('display: flex;', 'display: flex; align-items: center;')
            
        # 2. Add Checkbox if missing
        if 'entry-select' not in controls_inner:
            checkbox = f'\n                <input type="checkbox" class="entry-select" data-id="{entry_id}" onchange="refreshBatchUI()" style="width: 18px; height: 18px; cursor: pointer; margin-right: 10px;">'
            controls_inner = checkbox + controls_inner
            
        # 3. Add Copy Button if missing
        if 'copyEntry' not in controls_inner:
            copy_btn = f'\n                <button onclick="copyEntry(\'{entry_id}\')" class="control-btn copy-btn" title="Copy">📋</button>'
            controls_inner += copy_btn
            
        return f'<div class="harvest-entry" id="{entry_id}" {entry_style}>\n            <div class="entry-controls" style="{controls_style}">{controls_inner}'

    # Matches the outer div and the controls div specifically
    pattern = r'<div class="harvest-entry" id="([^"]+)"\s*(.*?)>\s*<div class="entry-controls"\s*style="([^"]+)">([\s\S]*?)(?=<button onclick="editEntry|<\/div>)'
    
    # We need to be careful with the trailing content. 
    # Let's try to just find the entry-controls div and its contents.
    
    def surgical_fix(content):
        # Find all entry IDs
        ids = re.findall(r'<div class="harvest-entry" id="([^"]+)"', content)
        for eid in ids:
            start_marker = f'<!-- ENTRY_START_{eid} -->'
            end_marker = f'<!-- ENTRY_END_{eid} -->'
            if start_marker in content and end_marker in content:
                parts = content.split(start_marker)
                entry_block, suffix = parts[1].split(end_marker)
                
                # Reconstruct entry_block with new UI
                if 'entry-select' not in entry_block:
                    # Update style
                    entry_block = entry_block.replace('display: flex; gap: 10px;', 'display: flex; gap: 10px; align-items: center;')
                    # Insert checkbox
                    checkbox = f'\n                <input type="checkbox" class="entry-select" data-id="{eid}" onchange="refreshBatchUI()" style="width: 18px; height: 18px; cursor: pointer; margin-right: 10px;">'
                    entry_block = entry_block.replace('onmouseout="this.style.opacity=0.2">', 'onmouseout="this.style.opacity=0.2">' + checkbox)
                
                if 'copyEntry' not in entry_block:
                    copy_btn = f'\n                <button onclick="copyEntry(\'{eid}\')" class="control-btn copy-btn" title="Copy">📋</button>'
                    entry_block = entry_block.replace(f"onclick=\"editEntry('{eid}')\"", f"onclick=\"copyEntry('{eid}')\" class=\"control-btn copy-btn\" title=\"Copy\">📋</button>\n                <button onclick=\"editEntry('{eid}')\"")
                
                content = parts[0] + start_marker + entry_block + end_marker + suffix
        return content

    new_content = surgical_fix(content)
    
    with open(MASTER_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully migrated master_harvest.html to Version 5.0 (Batch Operations Support).")
else:
    print("master_harvest.html not found, skipping migration.")
