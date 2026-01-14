@echo off
title AI Knowledge Capture - HARVEST MODE
cd /d "%~dp0"

echo ---------------------------------------------------
echo 🔥 KNOWLEDGE CAPTURE: HARVEST MODE ACTIVE
echo ---------------------------------------------------
echo [1/2] Starting Clipboard Monitor...
start /min powershell.exe -ExecutionPolicy Bypass -File "clipboard_capture.ps1" -AutoAppend

echo [2/2] Starting Web UI Server (Port 8000)...
start /min python -m http.server 8000

echo.
echo ✅ SYSTEM FULLY OPERATIONAL
echo.
echo [VIEW] -> http://localhost:8000/viewer.html
echo [FOLDER] -> %cd%
echo ---------------------------------------------------
echo.
echo TIPS:
echo - Copy any text (Ctrl+C) to save instantly.
echo - Use viewer.html in browser for ChatGPT-style UI.
echo - Close this window to stop monitoring.
echo.
pause
