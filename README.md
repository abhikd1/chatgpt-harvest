# 📚 Knowledge Capture System

**Two-mode AI response capture: Lossless Harvest + Quality-Checked Curation**

---

## 🎯 What This Is

A dual-mode system for capturing AI responses:

### 🔒 Harvest Mode (NEW)
**Character-perfect capture with ZERO mutation**
- Every emoji preserved: 🔥🚀🧠💡
- Every markdown element intact
- Every whitespace unchanged
- SHA-256 verified integrity
- **If even ONE character changes, the system FAILS**

### ✅ Quality Mode (Existing)
**Validated, curated knowledge archival**
- Removes conversational filler
- Enforces archival standards
- Validates code blocks
- Ensures self-containment

---

## 🚀 Quick Start

### Lossless Harvest Mode

```bash
# 1. Start harvest system
START_HARVEST.bat

# 2. In any AI chat (ChatGPT, Gemini, Claude):
#    - Select response (Ctrl+A)
#    - Press Ctrl+Shift+H
#    ✅ Saved to harvests/AI_HARVEST_001.txt

# 3. Check stats
python lossless_capture.py --stats
```

### Quality Mode

```bash
# Interactive capture with validation
python knowledge_capture.py append
# Paste content, Ctrl+Z, Enter
```

---

## ⌨️ Hotkeys

| Hotkey | Mode | Action |
|--------|------|--------|
| `Ctrl+Shift+H` | Harvest | Capture losslessly |
| `Ctrl+Shift+L` | Harvest | Show stats |
| `Ctrl+Shift+K` | Quality | Capture with validation |
| `Ctrl+Shift+S` | Quality | Show stats |

---

Automated quality enforcement for archival-grade Markdown content with clipboard integration.

## Features

- Markdown validation against archival standards
- Automatic clipboard monitoring
- Hotkey-based instant capture
- Quality scoring and statistics
- Self-containment verification
- Zero-dependency Python core

## Quick Start

### Option 1: Automatic Clipboard Monitoring (Recommended)

```powershell
START_MONITOR.bat
```

Copy any AI response → System auto-validates → Auto-appends if valid

### Option 2: Hotkey Capture

1. Install AutoHotkey v2
2. Run `hotkey_append.ahk`
3. Press `Ctrl+Shift+K` to capture clipboard

### Option 3: Manual Validation

```powershell
Get-Content myfile.md | python knowledge_capture.py validate
Get-Content myfile.md | python knowledge_capture.py append
```

## Installation

No dependencies required. Uses Python 3.7+ standard library.

Optional:
- AutoHotkey v2 (for hotkey method)
- PowerShell 5.1+ (built into Windows 10+)

## Usage

### Commands

```powershell
# Validate content
Get-Content file.md | python knowledge_capture.py validate

# Append to knowledge log
Get-Content file.md | python knowledge_capture.py append

# View statistics
python knowledge_capture.py stats
```

### Clipboard Integration

**Start automatic monitoring:**
```powershell
.\clipboard_capture.ps1 -AutoAppend
```

**Validation only (no auto-append):**
```powershell
.\clipboard_capture.ps1
```

**Hotkeys (requires AutoHotkey):**
- `Ctrl+Shift+K` - Capture clipboard
- `Ctrl+Shift+S` - Show stats

## Quality Standards

Content must meet:

- Top-level header required (`#`)
- Code blocks must specify language (` ```python `)
- No conversational artifacts ("Sure", "Here's", etc.)
- Self-contained (no "see above" references)
- Consistent formatting

## File Structure

```
knowledge_capture/
├── Core System
│   ├── knowledge_capture.py      Main CLI
│   ├── validator.py              Validation rules
│   ├── analyzer.py               Quality scoring
│   └── appender.py               File operations
├── Clipboard Integration
│   ├── clipboard_capture.ps1     Auto-monitor
│   ├── hotkey_append.ahk         Hotkey script
│   ├── quick_capture.bat         Manual capture
│   └── START_MONITOR.bat         Quick launcher
├── Documentation
│   ├── README.md                 This file
│   ├── USAGE.md                  Detailed guide
│   ├── system_prompt_addon.md    Qwen-style mode
│   └── capability_assessment.md  System analysis
└── Output
    └── knowledge_log.md          Your knowledge base
```

## Examples

### Valid Content

```markdown
# Topic Title

## Context

Brief context.

## Implementation

```python
def example():
    return "code"
```

## Key Points

- Point 1
- Point 2
```

### Invalid Content

```markdown
Sure, here's what you asked for...

Code without language:
```
code here
```

As mentioned earlier...
```

## Troubleshooting

### PowerShell Script Won't Run

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Python Not Found

Ensure Python is in PATH or use full path:
```powershell
C:\Python312\python.exe knowledge_capture.py stats
```

## Advanced

### Run on Startup

Create shortcut in Startup folder:
```
Target: powershell.exe -WindowStyle Hidden -File "...\clipboard_capture.ps1" -AutoAppend
```

### Custom Knowledge Directory

```powershell
.\clipboard_capture.ps1 -KnowledgeDir "D:\MyKnowledge" -AutoAppend
```

## Documentation

See `USAGE.md` for comprehensive guide including:
- Detailed workflows
- Integration tips
- Backup strategies
- Advanced configuration

