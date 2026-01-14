# 🔒 Lossless AI Response Harvest System - Usage Guide

**Philosophy**: Glass mirror - reflects without thinking, improving, or modifying.

---

## 🚀 Quick Start

### 1. Activate Harvest System

```bash
START_HARVEST.bat
```

**What happens**:
- ✅ Harvest hotkeys registered globally
- ✅ System tray icon appears
- ✅ Ready to capture

---

## ⌨️ Hotkeys

| Hotkey | Action |
|--------|--------|
| `Ctrl+Shift+H` | Capture selection (lossless) |
| `Ctrl+Shift+L` | Show harvest stats |

---

## 📋 Usage Workflows

### Workflow 1: Quick Harvest from Browser

1. **Get AI response** (ChatGPT, Gemini, Claude, etc.)
2. **Select all** (`Ctrl+A`)
3. **Press** `Ctrl+Shift+H`
4. ✅ **Done** - Saved to `harvests/AI_HARVEST_001.txt`

**Result**: Character-perfect capture with zero mutation.

---

### Workflow 2: Interactive Capture

```bash
python lossless_capture.py
```

1. Paste AI response
2. Press `Ctrl+Z` then `Enter`
3. Choose action:
   - `C` - Copy to clipboard
   - `S` - Save to file
   - `N` - New file
   - `X` - Ignore

---

### Workflow 3: Clipboard Capture

```bash
python lossless_capture.py --clipboard
```

**Use case**: Already copied AI response, just want to save it.

---

### Workflow 4: Check Stats

```bash
python lossless_capture.py --stats
```

**Shows**:
- Current harvest file
- Total harvest files
- Buffer status
- File sizes

---

## 📁 File Organization

```
knowledge_capture/
├── harvests/
│   ├── AI_HARVEST_001.txt  ← Raw AI responses (lossless)
│   ├── AI_HARVEST_002.txt
│   └── ...
└── knowledge_log.md        ← Quality-checked knowledge (curated)
```

---

## 🔄 Two Capture Modes

### Harvest Mode (NEW)
- **Hotkey**: `Ctrl+Shift+H`
- **Philosophy**: Zero transformation
- **Output**: `harvests/AI_HARVEST_XXX.txt`
- **Use case**: "I want EVERYTHING exactly as-is"

### Quality Mode (Existing)
- **Hotkey**: `Ctrl+Shift+K`
- **Philosophy**: Validated, curated
- **Output**: `knowledge_log.md`
- **Use case**: "I want clean, archival-grade knowledge"

---

## 🔒 Integrity Guarantee

Every capture is verified with:

✅ **Character count** match
✅ **Emoji count** match
✅ **Markdown fence** count match
✅ **Line break** count match
✅ **SHA-256 checksum** match

**If even ONE character differs, the system FAILS the save.**

---

## 💡 Pro Tips

### Tip 1: Start New File for New Topic

When switching topics:
```bash
# In interactive mode, press 'N'
# Or manually:
python lossless_capture.py
# Then press N
```

---

### Tip 2: Promote Harvest to Knowledge Log

After reviewing a harvest file:
```bash
# Copy content from AI_HARVEST_001.txt
# Then use quality mode:
python knowledge_capture.py append
```

---

### Tip 3: Batch Processing

Capture multiple AI responses rapidly:
1. `Ctrl+Shift+H` (capture #1)
2. `Ctrl+Shift+H` (capture #2)
3. `Ctrl+Shift+H` (capture #3)

All saved to same file with separators.

---

## 🧪 Testing Integrity

### Manual Test

1. Capture a complex AI response (with emojis, code, tables)
2. Open `harvests/AI_HARVEST_001.txt`
3. Compare character-by-character with original

**Expected**: Byte-identical match.

---

### Automated Test

```bash
python -m pytest tests/test_harvest_integrity.py
```

---

## ❓ FAQ

### Q: What if I want to edit captured content?

**A**: Harvest mode is for **archival**, not editing. If you want to edit:
1. Capture with harvest mode
2. Review the file
3. Copy relevant parts
4. Use quality mode to add to `knowledge_log.md`

---

### Q: Can I merge multiple harvest files?

**A**: Yes, manually:
```bash
type harvests\AI_HARVEST_001.txt harvests\AI_HARVEST_002.txt > merged.txt
```

---

### Q: What's the difference from existing capture?

| Feature | Harvest Mode | Quality Mode |
|---------|-------------|--------------|
| Transformation | ZERO | Validates & cleans |
| Output | `AI_HARVEST_XXX.txt` | `knowledge_log.md` |
| Headers required | No | Yes |
| Code fence tags | Preserved as-is | Required |
| Conversational filler | Preserved | Removed |

---

## 🎯 When to Use Which Mode

### Use Harvest Mode When:
- ✅ Capturing complex formatting (tables, emojis, code)
- ✅ Want to preserve EVERYTHING
- ✅ Rapid-fire capture during research
- ✅ Don't want to think about quality

### Use Quality Mode When:
- ✅ Building permanent knowledge base
- ✅ Want clean, archival-grade content
- ✅ Need validation and quality checks
- ✅ Creating reference documentation

---

## 🔥 Real-World Example

### Scenario: Processing 10 ChatGPT Responses

```bash
# 1. Start harvest system
START_HARVEST.bat

# 2. In ChatGPT, for each response:
#    - Select all (Ctrl+A)
#    - Press Ctrl+Shift+H

# 3. Check what was captured:
python lossless_capture.py --stats

# 4. Review harvests/AI_HARVEST_001.txt

# 5. If valuable, promote to knowledge log:
python knowledge_capture.py append
#    (paste content from harvest file)
```

**Result**: 
- ✅ 10 AI responses captured losslessly
- ✅ Reviewed at your pace
- ✅ Best ones promoted to knowledge base
- ✅ Zero information loss

---

## 🛠️ Troubleshooting

### Issue: Hotkeys not working

**Solution**:
```bash
# Restart harvest system
taskkill /F /IM AutoHotkey.exe
START_HARVEST.bat
```

---

### Issue: Integrity check failed

**Cause**: File was modified after save.

**Solution**: Re-capture the content.

---

### Issue: Missing pyperclip

**Solution**:
```bash
pip install pyperclip
```

---

## 📊 System Architecture

```
AI Response → Ctrl+Shift+H → harvest_engine.py → integrity_checker.py → AI_HARVEST_XXX.txt
                                     ↓
                              (zero transformation)
                                     ↓
                              SHA-256 verification
```

---

> [!IMPORTANT]
> **The Golden Rule**: If you change even ONE character, the system has FAILED.

---

> [!TIP]
> **Best Practice**: Use harvest mode for capture, quality mode for curation.
