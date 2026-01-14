import re
import os

def fix_viewer():
    path = 'viewer.html'
    if not os.path.exists(path): return

    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. THE EMOJI FIX - Convert ?? to real symbols
    emoji_map = {
        '?? Typography': '📝 Typography',
        '?? Callout': '📣 Callout',
        '?? Blockquotes': '💬 Blockquotes',
        '?? Status': '📊 Status',
        '?? Badges': '🎨 Badges',
        '?? Progress': '🏮 Progress',
        '?? Tooltips': '🎭 Tooltips',
        '?? Avatars': '🎨 Avatars',
        '?? Buttons': '🔥 Buttons',
        '?? Header': '🏮 Header',
        '?? Chat': '💬 Chat',
        '?? Content': '🎨 Content',
        '?? Stats': '📊 Stats',
        '?? Main': '🎯 Main',
        '?? Performance': '🎯 Performance',
        '?? Mission': '🚀 Mission',
        '?? Goal': '🎯 Goal',
        '?? Delivered': '📅 Delivered',
        '?? Lines': '⚡ Lines',
        '?? Style': '🎨 Style',
        '? Copied!': '✅ Copied!',
        '? Message copied': '📋 Message copied',
        '? Cancel': '❌ Cancel',
        '? Message updated!': '✏️ Message updated!',
        'id="stat-emojis">0': 'id="stat-emojis">🔥',
        'isUser ? \'👤\' : \'🤖\'': 'isUser ? "👤" : "🤖"',
        '?? Code Blocks': '💻 Code Blocks',
        '?? Tables': '📊 Tables',
        '?? Lists': '📋 Lists',
        '?? Emojis': '😊 Emojis'
    }
    
    for k, v in emoji_map.items():
        c = c.replace(k, v)

    # Generic fix for ?? Title patterns
    c = re.sub(r'\?\? ([A-Z][a-z]+)', r'✨ \1', c)

    # 2. THE SCROLL FIX
    # Make sure the body is scrollable
    c = c.replace('overflow-x: hidden;', 'overflow-x: hidden; overflow-y: auto !important;')
    c = c.replace('min-height: 100vh;', 'min-height: 100vh !important; height: auto !important;')
    
    # 3. STATS LOGIC FIX
    # We will use simple string replacement instead of re.sub for the logic block to avoid escape errors
    old_logic_part = "        // Update stats if they exist"
    new_logic_part = """
        // [MODIFIED STATS LOGIC]
        const stats_cards = document.querySelectorAll('.stat-card');
        stats_cards.forEach(card => {
            const label = card.querySelector('.stat-label');
            const num = card.querySelector('.stat-number');
            if (label && num) {
                const text_label = label.innerText.toLowerCase();
                if (text_label.includes('entries')) num.innerText = entries.length.toLocaleString();
                if (text_label.includes('emoji')) {
                    const count = (text.match(/[\\u{1F300}-\\u{1F9FF}]/gu) || []).length;
                    num.innerText = count.toLocaleString();
                }
            }
        });
        // [END STATS LOGIC]
    """
    
    # Find the block and replace it
    # We find between 'const entries = ...' and 'vault.innerHTML = "";'
    target_pattern = re.compile(r'const entries =.*?\n.*?vault\.innerHTML', re.DOTALL)
    match = target_pattern.search(c)
    if match:
        snippet = match.group(0)
        # Find the section to replace inside this snippet
        if "// Update stats" in snippet:
             # Find end of that logic
             # In the template it ends before vault.innerHTML
             pass

    # Simplified replacement:
    if "const entries =" in c and "vault.innerHTML =" in c:
        parts = c.split("vault.innerHTML = '';")
        head = parts[0]
        tail = parts[1]
        
        # Add the logic before clearing the vault
        head += new_logic_part
        c = head + "vault.innerHTML = '';" + tail

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("Viewer UI fixed: Emojis restored, Scroll enabled.")

if __name__ == "__main__":
    fix_viewer()
