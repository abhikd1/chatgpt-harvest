#!/usr/bin/env python3
"""
POST-PROCESSOR: Clean Monaco bloat from saved renders for lightning-fast loading
Run this on existing render files to make them load instantly
"""

import re
from pathlib import Path

def clean_monaco_bloat(html_content):
    """Remove Monaco editor DOM bloat from HTML"""
    
    # Pattern to match Monaco editor sections
    monaco_pattern = r'<div class="monaco-editor[^>]*>.*?</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>'
    
    # Extract code from Monaco and replace with simple pre/code
    def replace_monaco(match):
        monaco_html = match.group(0)
        # Try to extract the actual code text
        code_match = re.search(r'<span class="mtk\d+">(.*?)</span>', monaco_html)
        if code_match:
            code = code_match.group(1)
            # Unescape HTML entities
            code = code.replace('&nbsp;', ' ').replace('&quot;', '"').replace('&lt;', '<').replace('&gt;', '>')
            return f'<pre><code>{code}</code></pre>'
        return ''
    
    # Remove Monaco bloat
    cleaned = re.sub(monaco_pattern, replace_monaco, html_content, flags=re.DOTALL)
    
    # Remove SVG icons
    cleaned = re.sub(r'<svg[^>]*width="1em"[^>]*>.*?</svg>', '', cleaned, flags=re.DOTALL)
    
    # Remove empty divs
    cleaned = re.sub(r'<div[^>]*>\s*</div>', '', cleaned)
    
    return cleaned

def process_render_file(filepath):
    """Process a single render file"""
    print(f"Processing: {filepath.name}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_size = len(content)
    
    # Clean Monaco bloat
    cleaned = clean_monaco_bloat(content)
    
    new_size = len(cleaned)
    reduction = ((original_size - new_size) / original_size * 100) if original_size > 0 else 0
    
    # Save cleaned version
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned)
    
    print(f"  Size: {original_size:,} -> {new_size:,} bytes ({reduction:.1f}% reduction)")
    
    return original_size, new_size

def main():
    """Process all render files"""
    renders_dir = Path(__file__).parent / "renders"
    
    if not renders_dir.exists():
        print("No renders directory found!")
        return
    
    render_files = list(renders_dir.glob("RENDER_*.html"))
    
    if not render_files:
        print("No render files found!")
        return
    
    print(f"\nFound {len(render_files)} render files\n")
    print("=" * 60)
    
    total_original = 0
    total_new = 0
    
    for filepath in sorted(render_files):
        orig, new = process_render_file(filepath)
        total_original += orig
        total_new += new
    
    print("=" * 60)
    total_reduction = ((total_original - total_new) / total_original * 100) if total_original > 0 else 0
    print(f"\nTotal: {total_original:,} -> {total_new:,} bytes")
    print(f"Overall reduction: {total_reduction:.1f}%")
    print(f"\nAll files now load LIGHTNING FAST!")

if __name__ == '__main__':
    main()
