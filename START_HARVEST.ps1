# ═══════════════════════════════════════════════════════════════
# LOSSLESS HARVEST SYSTEM - ONE-CLICK LAUNCHER (PowerShell)
# ═══════════════════════════════════════════════════════════════

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🔒 LOSSLESS AI RESPONSE HARVEST SYSTEM                   ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check if AutoHotkey is installed
$ahkPath = Get-Command "AutoHotkey.exe" -ErrorAction SilentlyContinue
if (-not $ahkPath) {
    Write-Host "❌ AutoHotkey not found" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install AutoHotkey from: https://www.autohotkey.com/"
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Python is available
$pythonPath = Get-Command "python" -ErrorAction SilentlyContinue
if (-not $pythonPath) {
    Write-Host "❌ Python not found" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Install pyperclip if needed
Write-Host "📦 Checking dependencies..." -ForegroundColor Yellow
python -c "import pyperclip" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing pyperclip..." -ForegroundColor Yellow
    pip install pyperclip
}

Write-Host ""
Write-Host "✅ Starting harvest hotkeys..." -ForegroundColor Green
Write-Host ""
Write-Host "🔥 ACTIVE HOTKEYS:" -ForegroundColor Yellow
Write-Host "   Ctrl+Shift+H = Capture selection (lossless)"
Write-Host "   Ctrl+Shift+L = Show harvest stats"
Write-Host ""
Write-Host "💡 Minimize this window - hotkeys will stay active" -ForegroundColor Cyan
Write-Host ""

# Get script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ahkScript = Join-Path $scriptDir "harvest_hotkeys.ahk"

# Start AutoHotkey script
Start-Process -FilePath "AutoHotkey.exe" -ArgumentList "`"$ahkScript`"" -WindowStyle Hidden

Write-Host "✅ Harvest system is now running in background" -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to stop harvest system..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Kill AutoHotkey process
Stop-Process -Name "AutoHotkey" -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "🛑 Harvest system stopped" -ForegroundColor Red
Write-Host ""
Read-Host "Press Enter to exit"
