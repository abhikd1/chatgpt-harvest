"""
SIMPLE RENDER CAPTURE - No server needed!

This version saves HTML directly to clipboard, then you paste into a file.
Much simpler than the server approach.
"""

import sys
import os
import pyperclip
from datetime import datetime
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def create_html_wrapper(content, source="Unknown"):
    """Wrap content in full HTML document"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Render Capture - {timestamp}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .metadata {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 30px;
            font-size: 0.9em;
            color: #666;
        }}
        .content {{
            font-size: 16px;
        }}
        .content h1 {{ font-size: 2em; margin: 1em 0 0.5em; }}
        .content h2 {{ font-size: 1.5em; margin: 1.2em 0 0.6em; }}
        .content h3 {{ font-size: 1.2em; margin: 1em 0 0.5em; }}
        .content code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Consolas', monospace;
            font-size: 0.9em;
        }}
        .content pre {{
            background: #282c34;
            color: #abb2bf;
            padding: 20px;
            border-radius: 6px;
            overflow-x: auto;
        }}
        .content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5em 0;
        }}
        .content table th, .content table td {{
            padding: 12px;
            border: 1px solid #dee2e6;
        }}
        .content table th {{
            background: #f8f9fa;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="metadata">
            <strong>Source:</strong> {source}<br>
            <strong>Captured:</strong> {timestamp}
        </div>
        <div class="content">
{content}
        </div>
    </div>
</body>
</html>"""


def save_from_clipboard():
    """Get HTML from clipboard and save as file"""
    try:
        # Get from clipboard
        content = pyperclip.paste()
        
        if not content or len(content) < 10:
            print("❌ Clipboard is empty or too short")
            return
        
        # Create full HTML
        html = create_html_wrapper(content, source="Clipboard")
        
        # Save to file
        renders_dir = Path(__file__).parent / "renders"
        renders_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"RENDER_{timestamp}.html"
        filepath = renders_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Saved render to: {filepath}")
        print(f"   📊 Size: {len(html)} bytes")
        print(f"\n💡 Open with: start {filepath}")
        
        return filepath
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


if __name__ == '__main__':
    print("\n" + "="*60)
    print("📸 SIMPLE RENDER CAPTURE")
    print("="*60)
    print("\nThis captures HTML from clipboard and saves as a file.\n")
    print("Instructions:")
    print("1. In ChatGPT, right-click the response")
    print("2. Choose 'Inspect' or 'Inspect Element'")
    print("3. In DevTools, right-click the element")
    print("4. Choose 'Copy' → 'Copy outerHTML'")
    print("5. Run this script\n")
    
    input("Press Enter when you've copied the HTML...")
    
    filepath = save_from_clipboard()
    
    if filepath:
        print(f"\n🎉 Success! Opening file...")
        os.system(f'start "" "{filepath}"')
