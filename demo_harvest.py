"""
QUICK DEMO - Test the lossless harvest system

This script demonstrates:
1. Capturing complex AI responses
2. Preserving emojis, markdown, tables, code
3. Verifying integrity
"""

import sys
import os

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from response_buffer import store_response
from harvest_file_manager import save_to_current_file, get_current_file_path


# Sample AI response with complex formatting
SAMPLE_AI_RESPONSE = """# 🚀 Advanced Python Optimization Techniques

Here are **5 proven methods** to optimize your Python code:

## 1. Use List Comprehensions 💡

```python
# Slow
result = []
for i in range(1000):
    result.append(i * 2)

# Fast
result = [i * 2 for i in range(1000)]
```

## 2. Leverage Built-in Functions ⚡

| Function | Use Case | Speed Gain |
|----------|----------|------------|
| `map()` | Transform iterables | 2-3x |
| `filter()` | Filter iterables | 2x |
| `sum()` | Sum numbers | 5x |

## 3. Profile Your Code 🔍

Use `cProfile` to find bottlenecks:

```python
import cProfile
cProfile.run('your_function()')
```

## 4. Use Generators for Large Data 🌊

```python
def large_dataset():
    for i in range(1_000_000):
        yield process(i)
```

## 5. Multiprocessing for CPU-Bound Tasks 🖥️

```python
from multiprocessing import Pool

with Pool(4) as p:
    results = p.map(cpu_intensive_task, data)
```

---

**Pro Tip**: Always measure before optimizing! 📊

Unicode test: 世界 مرحبا мир 🌍
"""


def main():
    print("\n" + "="*60)
    print("🔒 LOSSLESS HARVEST SYSTEM - DEMO")
    print("="*60 + "\n")
    
    print("📝 Sample AI Response:")
    print("-" * 60)
    print(SAMPLE_AI_RESPONSE[:200] + "...")
    print("-" * 60)
    print(f"\nTotal length: {len(SAMPLE_AI_RESPONSE)} characters\n")
    
    # Capture the response
    print("🔄 Capturing response...")
    result = store_response(SAMPLE_AI_RESPONSE)
    
    print(f"✅ Captured successfully!")
    print(f"   📊 Characters: {result.char_count}")
    print(f"   😀 Emojis: {result.emoji_count}")
    print(f"   💻 Code blocks: {result.markdown_fence_count // 2}")
    print(f"   📄 Lines: {result.line_break_count + 1}")
    print(f"   🔒 Checksum: {result.checksum[:16]}...\n")
    
    # Save to file
    print("💾 Saving to harvest file...")
    success, _ = save_to_current_file(result)
    
    if success:
        file_path = get_current_file_path()
        print(f"✅ Saved to: {file_path}")
        
        # Verify by reading back
        print("\n🔍 Verifying integrity...")
        with open(file_path, 'rb') as f:
            saved_content = f.read().decode('utf-8')
        
        if saved_content == SAMPLE_AI_RESPONSE:
            print("✅ PERFECT MATCH - Zero mutation!")
            print("   Every character, emoji, and whitespace preserved exactly.\n")
        else:
            print("❌ Mismatch detected!")
            print(f"   Original: {len(SAMPLE_AI_RESPONSE)} chars")
            print(f"   Saved: {len(saved_content)} chars\n")
    else:
        print("❌ Save failed\n")
    
    print("="*60)
    print("🎉 DEMO COMPLETE")
    print("="*60)
    print("\nNext steps:")
    print("  1. Run: START_HARVEST.bat")
    print("  2. Press Ctrl+Shift+H to capture any AI response")
    print("  3. Check harvests/ folder for saved files\n")


if __name__ == '__main__':
    main()
