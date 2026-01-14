# 🔒 Lossless AI Response Harvest System

**Character-perfect AI response capture with zero mutation.**

---

## 🎯 What This Is

A **glass mirror system** that captures AI responses (ChatGPT, Gemini, Claude, etc.) with **absolute fidelity**:

- ✅ Every emoji preserved: 🔥🚀🧠💡
- ✅ Every markdown element intact
- ✅ Every whitespace character unchanged
- ✅ Every Unicode character preserved
- ✅ SHA-256 verified integrity

**If even ONE character changes, the system FAILS.**

---

## 🚀 Quick Start

### 1. Launch Harvest System

```bash
START_HARVEST.bat
```

### 2. Capture AI Response

1. Get AI response in browser/ChatGPT/etc.
2. Select all (`Ctrl+A`)
3. Press `Ctrl+Shift+H`
4. ✅ Done - saved to `harvests/AI_HARVEST_001.txt`

---

## ⌨️ Hotkeys

| Hotkey | Action |
|--------|--------|
| `Ctrl+Shift+H` | Capture selection (lossless) |
| `Ctrl+Shift+L` | Show harvest stats |

---

## 📁 File Structure

```
knowledge_capture/
├── harvests/
│   ├── AI_HARVEST_001.txt  ← Lossless captures
│   ├── AI_HARVEST_002.txt
│   └── ...
└── knowledge_log.md        ← Quality-checked knowledge
```

---

## 🔄 Two Capture Modes

### 🔒 Harvest Mode (NEW)
- **Hotkey**: `Ctrl+Shift+H`
- **Philosophy**: Zero transformation
- **Output**: `harvests/AI_HARVEST_XXX.txt`
- **Use**: "I want EVERYTHING exactly as-is"

### ✅ Quality Mode (Existing)
- **Hotkey**: `Ctrl+Shift+K`
- **Philosophy**: Validated, curated
- **Output**: `knowledge_log.md`
- **Use**: "I want clean, archival-grade knowledge"

---

## 📋 Usage Examples

### Example 1: Quick Capture from ChatGPT

```
1. Get ChatGPT response
2. Ctrl+A (select all)
3. Ctrl+Shift+H (harvest)
✅ Saved losslessly
```

### Example 2: Interactive Capture

```bash
python lossless_capture.py
# Paste content
# Ctrl+Z then Enter
# Press S to save
```

### Example 3: Promote to Knowledge Log

```bash
# List harvest files
python harvest_bridge.py list

# Promote to knowledge log
python harvest_bridge.py promote harvests/AI_HARVEST_001.txt
```

---

## 🧪 Verify Integrity

```bash
python test_harvest_integrity.py
```

**Tests**:
- ✅ Emoji preservation
- ✅ Markdown preservation
- ✅ Whitespace preservation
- ✅ Unicode preservation
- ✅ Checksum validation

---

## 🔒 Integrity Guarantee

Every capture is verified with:

| Check | Description |
|-------|-------------|
| Character count | Exact match |
| Emoji count | Exact match |
| Markdown fences | Exact match |
| Line breaks | Exact match |
| SHA-256 checksum | Byte-identical |

---

## 📚 Components

| File | Purpose |
|------|---------|
| `harvest_engine.py` | Core lossless capture engine |
| `response_buffer.py` | In-memory response storage |
| `integrity_checker.py` | Verification system |
| `harvest_file_manager.py` | Auto-numbered file management |
| `lossless_capture.py` | Main CLI interface |
| `harvest_hotkeys.ahk` | Global keyboard shortcuts |
| `harvest_bridge.py` | Promote to knowledge log |
| `START_HARVEST.bat` | One-click launcher |

---

## 💡 Philosophy

> "I am a glass mirror.  
> I do not think.  
> I do not improve.  
> I do not modify.  
> I only reflect."

---

## 📖 Full Documentation

See [HARVEST_USAGE.md](HARVEST_USAGE.md) for complete usage guide.

---

## 🎯 When to Use

**Use Harvest Mode** for:
- Complex formatting (tables, emojis, code)
- Rapid-fire capture during research
- Preserving EVERYTHING without thinking

**Use Quality Mode** for:
- Building permanent knowledge base
- Clean, archival-grade content
- Reference documentation

---

## ⚡ Pro Tip

**Workflow**: Harvest first, curate later.

1. `Ctrl+Shift+H` - Capture everything losslessly
2. Review `harvests/AI_HARVEST_001.txt` at your pace
3. Promote valuable content to `knowledge_log.md`

**Result**: Zero information loss + curated knowledge base.

---

> **The Golden Rule**: If you change even ONE character, the system has FAILED.
