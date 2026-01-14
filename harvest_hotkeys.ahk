; ═══════════════════════════════════════════════════════════════
; LOSSLESS HARVEST HOTKEYS
; 
; Philosophy: One-key capture without mutation
; ═══════════════════════════════════════════════════════════════

#NoEnv
#SingleInstance Force
SetWorkingDir %A_ScriptDir%

; ───────────────────────────────────────────────────────────────
; GLOBAL HOTKEYS
; ───────────────────────────────────────────────────────────────

; Ctrl+Shift+H - Activate Harvest Mode (capture from clipboard)
^+h::
    Send ^c  ; Copy selected text
    Sleep 100
    RunWait, python lossless_capture.py --clipboard, , Hide
    TrayTip, Harvest Mode, Content captured and saved, 2, 1
return

; Ctrl+Shift+L - Show Harvest Stats
^+l::
    Run, python lossless_capture.py --stats
return

; ───────────────────────────────────────────────────────────────
; SYSTEM TRAY MENU
; ───────────────────────────────────────────────────────────────

Menu, Tray, NoStandard
Menu, Tray, Add, 🔒 Harvest Mode Active, DoNothing
Menu, Tray, Add
Menu, Tray, Add, Capture Selection (Ctrl+Shift+H), CaptureSelection
Menu, Tray, Add, Show Stats (Ctrl+Shift+L), ShowStats
Menu, Tray, Add
Menu, Tray, Add, Exit, ExitScript

; ───────────────────────────────────────────────────────────────
; MENU HANDLERS
; ───────────────────────────────────────────────────────────────

DoNothing:
return

CaptureSelection:
    Send ^+h
return

ShowStats:
    Send ^+l
return

ExitScript:
    ExitApp
return

; ───────────────────────────────────────────────────────────────
; STARTUP MESSAGE
; ───────────────────────────────────────────────────────────────

TrayTip, Lossless Harvest, Hotkeys active`nCtrl+Shift+H = Capture`nCtrl+Shift+L = Stats, 3, 1
