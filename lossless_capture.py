"""
LOSSLESS CAPTURE - Main CLI for harvest system

Usage:
    python lossless_capture.py              # Interactive mode
    python lossless_capture.py --clipboard  # Capture from clipboard
    python lossless_capture.py --stats      # Show stats
"""

import sys
import os

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import pyperclip
from response_buffer import (
    store_response, 
    get_content_for_clipboard,
    get_content_for_save,
    clear_buffer,
    has_buffered_content,
    get_buffer_stats
)
from harvest_file_manager import (
    save_to_current_file,
    start_new_file,
    get_current_file_path,
    get_file_stats,
    list_all_harvests
)


CONTROL_FOOTER = """────────────────────────
[PRESS: C]  → COPY EXACT RESPONSE
[PRESS: S]  → SAVE TO CURRENT FILE
[PRESS: N]  → START NEW FILE
[PRESS: X]  → IGNORE
────────────────────────"""


def show_control_footer():
    """Display control footer"""
    print(CONTROL_FOOTER)


def handle_copy():
    """Copy exact response to clipboard"""
    content = get_content_for_clipboard()
    if content:
        pyperclip.copy(content)
        stats = get_buffer_stats()
        print(f"✅ Copied {stats['characters']} chars to clipboard")
        print(f"   📊 {stats['emojis']} emojis, {stats['code_blocks']} code blocks, {stats['lines']} lines")
    else:
        print("❌ No content in buffer")


def handle_save():
    """Save to current harvest file"""
    from response_buffer import get_current_response
    
    capture_result = get_current_response()
    if not capture_result:
        print("❌ No content in buffer")
        return
    
    success, _ = save_to_current_file(capture_result)
    
    if success:
        file_path = get_current_file_path()
        stats = get_buffer_stats()
        print(f"✅ Saved to {file_path}")
        print(f"   📊 {stats['characters']} chars, {stats['emojis']} emojis, {stats['code_blocks']} code blocks")
        print(f"   🔒 Checksum: {capture_result.checksum[:16]}...")
        clear_buffer()
    else:
        print("❌ Save failed")


def handle_new_file():
    """Start new harvest file"""
    new_path = start_new_file()
    print(f"📄 Started new file: {new_path}")


def handle_ignore():
    """Discard current buffer"""
    clear_buffer()
    print("🗑️  Buffer cleared")


def show_stats():
    """Show harvest system stats"""
    print("\n📊 HARVEST SYSTEM STATS\n")
    
    # Current file stats
    file_stats = get_file_stats()
    print(f"Current File: {file_stats['file']}")
    if file_stats['exists']:
        print(f"  Size: {file_stats['size_kb']} KB")
        print(f"  Lines: {file_stats['lines']}")
    else:
        print(f"  Status: Not yet created")
    
    # All harvest files
    all_harvests = list_all_harvests()
    print(f"\nTotal Harvest Files: {len(all_harvests)}")
    
    if all_harvests:
        print("\nRecent Harvests:")
        for h in all_harvests[-5:]:  # Last 5
            print(f"  • {h['file']} ({h['size_kb']} KB)")
    
    # Buffer stats
    if has_buffered_content():
        print("\n📋 Current Buffer:")
        stats = get_buffer_stats()
        print(f"  Characters: {stats['characters']}")
        print(f"  Emojis: {stats['emojis']}")
        print(f"  Code Blocks: {stats['code_blocks']}")
        print(f"  Lines: {stats['lines']}")
    else:
        print("\n📋 Buffer: Empty")


def interactive_mode():
    """Interactive capture mode"""
    print("\n🔒 LOSSLESS HARVEST MODE ACTIVATED\n")
    print("Paste AI response below (Ctrl+Z then Enter when done):\n")
    
    # Read multiline input
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    
    content = '\n'.join(lines)
    
    if not content.strip():
        print("❌ No content provided")
        return
    
    # Store in buffer
    store_response(content)
    
    print("\n✅ Content captured in buffer\n")
    show_control_footer()
    
    # Wait for user action
    while has_buffered_content():
        action = input("\nAction: ").strip().upper()
        
        if action == 'C':
            handle_copy()
        elif action == 'S':
            handle_save()
            break
        elif action == 'N':
            handle_new_file()
        elif action == 'X':
            handle_ignore()
            break
        else:
            print("Invalid action. Use C/S/N/X")


def clipboard_mode():
    """Capture from clipboard"""
    content = pyperclip.paste()
    
    if not content.strip():
        print("❌ Clipboard is empty")
        return
    
    # Store in buffer
    result = store_response(content)
    
    print(f"✅ Captured from clipboard")
    print(f"   📊 {result.char_count} chars, {result.emoji_count} emojis")
    
    # Auto-save
    success, _ = save_to_current_file(result)
    
    if success:
        file_path = get_current_file_path()
        print(f"✅ Saved to {file_path}")
        print(f"   🔒 Checksum: {result.checksum[:16]}...")
    else:
        print("❌ Save failed")


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        if sys.argv[1] == '--clipboard':
            clipboard_mode()
        elif sys.argv[1] == '--stats':
            show_stats()
        else:
            print("Usage:")
            print("  python lossless_capture.py              # Interactive mode")
            print("  python lossless_capture.py --clipboard  # Capture from clipboard")
            print("  python lossless_capture.py --stats      # Show stats")
    else:
        interactive_mode()


if __name__ == '__main__':
    main()
