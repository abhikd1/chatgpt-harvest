@echo off
REM ========================================
REM START RENDER CAPTURE SERVER
REM ========================================

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║  🎨 RENDER CAPTURE SERVER - STARTING                      ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM Check if Python is available
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python not found
    pause
    exit /b 1
)

echo ✅ Starting server on http://localhost:8765
echo.
echo 📋 INSTRUCTIONS:
echo    1. Leave this window open
echo    2. Create bookmarklet in browser (see RENDER_MODE_GUIDE.md)
echo    3. Click bookmarklet on ChatGPT/Gemini responses
echo    4. Files saved to renders/ folder
echo.
echo ⚠️  Press Ctrl+C to stop server
echo.

REM Start the server
python capture_server.py

pause
