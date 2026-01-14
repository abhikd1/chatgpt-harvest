# Knowledge Capture System - Usage Guide

## Quick Start

### Method 1: Automatic Clipboard Monitoring (Recommended)

**Start the monitor:**

```powershell
cd "c:\Users\sumit\10 min plus youtube video ss\knowledge_capture"
.\clipboard_capture.ps1 -AutoAppend
```

**Workflow:**
1. Copy AI response (Ctrl+C)
2. System auto-validates
3. If valid → auto-appends to knowledge log
4. Notification confirms capture

**Stop monitoring:** Press Ctrl+C in PowerShell window

### Method 2: Hotkey Capture

**Requirements:** Install AutoHotkey v2 from https://www.autohotkey.com/

**Start the script:**
```
Double-click hotkey_append.ahk
```

**Hotkeys:**
- `Ctrl+Shift+K` - Capture clipboard to knowledge log
- `Ctrl+Shift+S` - Show knowledge log statistics

**Workflow:**
1. Copy AI response (Ctrl+C)
2. Press Ctrl+Shift+K
3. Tray notification shows result

### Method 3: Manual Batch File (No Dependencies)

**Run:**
```
Double-click quick_capture.bat
```

**Workflow:**
1. Paste content into window
2. Press Ctrl+Z, then Enter
3. Review validation result
4. Confirm append (Y/N)

## Validation Rules

Content must meet these standards:

| Rule | Requirement |
|------|-------------|
| Headers | Must start with `#` header |
| Code blocks | Must specify language (` ```python `) |
| Conversational text | No "Sure", "Here's", "As an AI" |
| References | No "see above", "mentioned earlier" |
| Self-containment | Complete without external context |

## File Structure

```
knowledge_capture/
├── knowledge_capture.py      (Core validator)
├── validator.py              (Validation rules)
├── analyzer.py               (Quality scoring)
├── appender.py               (File operations)
├── clipboard_capture.ps1     (Auto-monitor)
├── hotkey_append.ahk         (Hotkey script)
├── quick_capture.bat         (Manual capture)
├── knowledge_log.md          (Your knowledge base)
└── USAGE.md                  (This file)
```

## Common Commands

### View Statistics

```powershell
python knowledge_capture.py stats
```

### Validate a File

```powershell
Get-Content myfile.md | python knowledge_capture.py validate
```

### Manually Append a File

```powershell
Get-Content myfile.md | python knowledge_capture.py append
```

## Troubleshooting

### PowerShell Script Won't Run

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### AutoHotkey Not Working

- Ensure AutoHotkey v2 is installed
- Right-click script → Run as Administrator

### Python Not Found

- Ensure Python is in PATH
- Or use full path: `C:\Python312\python.exe`

## Tips

### Best Practice Workflow

1. Start `clipboard_capture.ps1 -AutoAppend` in morning
2. Copy valuable AI responses throughout day
3. System auto-validates and captures
4. Review `knowledge_log.md` at end of day

### Selective Capture

Run without `-AutoAppend` to validate only:

```powershell
.\clipboard_capture.ps1
```

System will show validation results but not auto-append.

### Backup Your Knowledge Log

```powershell
Copy-Item knowledge_log.md "knowledge_log_backup_$(Get-Date -Format 'yyyyMMdd').md"
```

## Integration with AI Chat

### Copy AI Response

1. Select entire AI response
2. Press Ctrl+C
3. System captures automatically (if monitor running)
4. Or press Ctrl+Shift+K (if using hotkey method)

### Verify Capture

```powershell
python knowledge_capture.py stats
```

Check that entry count increased.

## Advanced Usage

### Custom Knowledge Directory

```powershell
.\clipboard_capture.ps1 -KnowledgeDir "D:\MyKnowledge" -AutoAppend
```

### Run on Startup

Create shortcut in:
```
C:\Users\sumit\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
```

Target:
```
powershell.exe -WindowStyle Hidden -File "c:\Users\sumit\10 min plus youtube video ss\knowledge_capture\clipboard_capture.ps1" -AutoAppend
```

## Status Indicators

| Message | Meaning |
|---------|---------|
| `[OK]` | Success |
| `[ERROR]` | Validation failed |
| `[WARN]` | Content detected but invalid |
| `[INFO]` | Informational message |
| `[DETECT]` | Markdown content found |
| `[STATS]` | Statistics output |
