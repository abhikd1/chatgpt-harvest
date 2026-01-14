import re
import os

MASTER_FILE = "master_harvest.html"

if os.path.exists(MASTER_FILE):
    with open(MASTER_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    def inject_tldr(match):
        eid = match.group(1)
        meta_block = match.group(2)
        rest = match.group(3)
        
        if 'tldr-container' in rest:
            return match.group(0)
            
        tldr_block = f"""
            <div class="tldr-container" style="background: rgba(59, 130, 246, 0.05); border-left: 3px solid #3b82f6; padding: 10px 15px; margin-bottom: 15px; font-size: 13px; font-style: italic; color: var(--text-primary);">
                <strong>⚡ AI TL;DR:</strong> <span class="tldr-content" id="tldr-{eid}">Migration Note: Click Settings > Regenerate or edit entry to generate AI summary.</span>
            </div>"""
        
        return f'<!-- ENTRY_START_{eid} -->{meta_block}{tldr_block}{rest}'

    # Pattern to find start of entry and inject after metadata
    pattern = r'<!-- ENTRY_START_([a-f0-9\-]+) -->([\s\S]*?<div class="metadata"[\s\S]*?<\/div>)([\s\S]*?<!-- ENTRY_END_)'
    new_content = re.sub(pattern, inject_tldr, content, flags=re.DOTALL)
    
    with open(MASTER_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully migrated master_harvest.html to Version 6.0 (AI TL;DR Support).")
else:
    print("master_harvest.html not found, skipping migration.")
