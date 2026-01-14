; Knowledge Capture - Hotkey Integration (HARVEST MODE)
; Press Ctrl+Shift+K to capture clipboard instantly - ALL FILTERS REMOVED

#SingleInstance Force

KnowledgeDir := "c:\Users\sumit\10 min plus youtube video ss\knowledge_capture"

^+k::  ; Ctrl+Shift+K
{
    clipboard := ""
    Send ^c
    ClipWait 1
    
    if (clipboard = "") {
        TrayTip "Knowledge Capture", "No content in clipboard", 1
        return
    }
    
    ; REMOVED: Header checks and validation filters
    tempFile := A_Temp "\clipboard_temp.md"
    FileDelete %tempFile%
    FileAppend %clipboard%, %tempFile%, UTF-8
    
    ; Force append without validation - passing file path directly for perfect Unicode
    RunWait cmd /c "python ""%KnowledgeDir%\knowledge_capture.py"" append ""%tempFile%"" --force", , Hide
    
    if (ErrorLevel = 0) {
        TrayTip "Knowledge Captured", "Raw content harvested to log", 1
    } else {
        TrayTip "Knowledge Capture Failed", "Append error", 2
    }
    
    FileDelete %tempFile%
    return
}

^+s::  ; Ctrl+Shift+S - Show stats
{
    KnowledgeDir := "c:\Users\sumit\10 min plus youtube video ss\knowledge_capture"
    RunWait cmd /c "python ""%KnowledgeDir%\knowledge_capture.py"" stats & pause", , 
    return
}
