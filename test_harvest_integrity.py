"""
INTEGRITY TEST - Verify lossless capture works perfectly

Tests:
1. Emoji preservation
2. Markdown preservation
3. Whitespace preservation
4. Unicode preservation
5. Checksum validation
"""

import sys
import os

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from harvest_engine import capture, remove_footer
from response_buffer import store_response
from harvest_file_manager import save_to_current_file
from integrity_checker import verify_integrity


def test_emoji_preservation():
    """Test that emojis are preserved exactly"""
    content = "🔥 This is a test 🚀 with emojis 🧠💡✨"
    
    result = capture(content)
    
    # Regex counts emoji sequences, not individual emojis
    # "🔥", "🚀", "🧠💡✨" = 3 sequences
    assert result.emoji_count == 3, f"Expected 3 emoji sequences, got {result.emoji_count}"
    assert result.content.decode('utf-8') == content, "Content mismatch"
    
    print("✅ Emoji preservation test PASSED")


def test_markdown_preservation():
    """Test that markdown is preserved exactly"""
    content = """# Header

```python
def hello():
    print("world")
```

| Column 1 | Column 2 |
|----------|----------|
| Data     | More     |
"""
    
    result = capture(content)
    
    assert result.markdown_fence_count == 2, f"Expected 2 fences, got {result.markdown_fence_count}"
    assert '|' in result.content.decode('utf-8'), "Table pipes missing"
    
    print("✅ Markdown preservation test PASSED")


def test_whitespace_preservation():
    """Test that whitespace is preserved exactly"""
    content = "Line 1\n\nLine 3\t\tTabbed\n    Spaces"
    
    result = capture(content)
    
    decoded = result.content.decode('utf-8')
    assert decoded == content, "Whitespace mismatch"
    assert '\t\t' in decoded, "Tabs missing"
    assert '    ' in decoded, "Spaces missing"
    
    print("✅ Whitespace preservation test PASSED")


def test_unicode_preservation():
    """Test that Unicode characters are preserved"""
    content = "Hello 世界 مرحبا мир 🌍"
    
    result = capture(content)
    
    decoded = result.content.decode('utf-8')
    assert decoded == content, "Unicode mismatch"
    assert '世界' in decoded, "Chinese missing"
    assert 'مرحبا' in decoded, "Arabic missing"
    assert 'мир' in decoded, "Cyrillic missing"
    
    print("✅ Unicode preservation test PASSED")


def test_footer_removal():
    """Test that footer is removed correctly"""
    content = """AI response here

────────────────────────
[PRESS: C]  → COPY EXACT RESPONSE
[PRESS: S]  → SAVE TO CURRENT FILE
[PRESS: N]  → START NEW FILE
[PRESS: X]  → IGNORE
────────────────────────"""
    
    clean = remove_footer(content)
    
    assert '[PRESS: C]' not in clean, "Footer not removed"
    assert 'AI response here' in clean, "Content removed"
    
    print("✅ Footer removal test PASSED")


def test_checksum_consistency():
    """Test that checksum is consistent"""
    content = "Test content 🔥"
    
    result1 = capture(content)
    result2 = capture(content)
    
    assert result1.checksum == result2.checksum, "Checksums don't match"
    
    print("✅ Checksum consistency test PASSED")


def test_end_to_end_capture():
    """Test full capture workflow"""
    content = """# AI Response Test 🚀

This is a **complex** response with:

- Emojis: 🔥💡✨
- Code blocks:

```python
def test():
    return "hello"
```

- Tables:

| Feature | Status |
|---------|--------|
| Emojis  | ✅     |
| Code    | ✅     |

And some Unicode: 世界 مرحبا мир
"""
    
    # Store in buffer
    result = store_response(content)
    
    # Save to file
    success, _ = save_to_current_file(result)
    
    assert success, "Save failed"
    
    print("✅ End-to-end capture test PASSED")
    print(f"   📊 {result.char_count} chars, {result.emoji_count} emojis")
    print(f"   🔒 Checksum: {result.checksum[:16]}...")


def run_all_tests():
    """Run all integrity tests"""
    print("\n" + "="*60)
    print("🧪 LOSSLESS HARVEST INTEGRITY TESTS")
    print("="*60 + "\n")
    
    tests = [
        test_emoji_preservation,
        test_markdown_preservation,
        test_whitespace_preservation,
        test_unicode_preservation,
        test_footer_removal,
        test_checksum_consistency,
        test_end_to_end_capture,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__} ERROR: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"📊 RESULTS: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED - System is lossless!")
    else:
        print("⚠️  Some tests failed - system may have mutations")
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
