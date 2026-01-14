@echo off
REM ═══════════════════════════════════════════════════════════════
REM LOSSLESS HARVEST SYSTEM - ONE-CLICK LAUNCHER
REM ═══════════════════════════════════════════════════════════════

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║  🔒 LOSSLESS AI RESPONSE HARVEST SYSTEM                   ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM Check if AutoHotkey is installed
where ahk >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ AutoHotkey not found
    echo.
    echo Please install AutoHotkey from: https://www.autohotkey.com/
    echo.
    pause
    exit /b 1
)

REM Check if Python is available
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python not found
    pause
    exit /b 1
)

REM Install pyperclip if needed
echo 📦 Checking dependencies...
python -c "import pyperclip" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing pyperclip...
    pip install pyperclip
)

echo.
echo ✅ Starting harvest hotkeys...
echo.
echo 🔥 ACTIVE HOTKEYS:
echo    Ctrl+Shift+H = Capture selection (lossless)
echo    Ctrl+Shift+L = Show harvest stats
echo.
echo 💡 Minimize this window - hotkeys will stay active
echo.

REM Start AutoHotkey script
start "" "%~dp0harvest_hotkeys.ahk"

echo ✅ Harvest system is now running in background
echo.
echo Press any key to stop harvest system...
pause >nul

REM Kill AutoHotkey process
taskkill /F /IM AutoHotkey.exe >nul 2>nul

echo.
echo 🛑 Harvest system stopped
echo.
pause
