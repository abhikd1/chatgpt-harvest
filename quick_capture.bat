@echo off
setlocal enabledelayedexpansion

set KNOWLEDGE_DIR=c:\Users\sumit\10 min plus youtube video ss\knowledge_capture
set TEMP_FILE=%TEMP%\clipboard_temp.md

echo [INFO] Paste your content, then press Ctrl+Z and Enter
echo.

type con > "%TEMP_FILE%"

echo.
echo [INFO] Validating content...

python "%KNOWLEDGE_DIR%\knowledge_capture.py" validate < "%TEMP_FILE%"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [OK] Content is valid. Append to knowledge log? (Y/N)
    set /p CONFIRM=
    
    if /i "!CONFIRM!"=="Y" (
        python "%KNOWLEDGE_DIR%\knowledge_capture.py" append < "%TEMP_FILE%"
        echo [OK] Entry added to knowledge log
    ) else (
        echo [INFO] Cancelled
    )
) else (
    echo [ERROR] Content does not meet archival standards
)

del "%TEMP_FILE%" 2>nul
pause
