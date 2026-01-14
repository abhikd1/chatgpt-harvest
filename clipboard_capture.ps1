# Knowledge Capture - HARVEST MODE
# No filters. No validation. Saves everything you copy.

param(
    [string]$KnowledgeDir = "c:\Users\sumit\10 min plus youtube video ss\knowledge_capture",
    [switch]$AutoAppend = $true
)

Add-Type -AssemblyName System.Windows.Forms
$lastClipboard = ""

Write-Host "[OK] HARVEST MODE ACTIVE"
Write-Host "[INFO] Saving all copies to knowledge_log.md"
Write-Host "[INFO] Press Ctrl+C to stop"

while ($true) {
    Start-Sleep -Milliseconds 500
    try {
        $currentClipboard = [System.Windows.Forms.Clipboard]::GetText()
        
        if ($currentClipboard -and $currentClipboard -ne $lastClipboard) {
            $lastClipboard = $currentClipboard
            
            # Force UTF8 for the session to preserve emojis across pipes
            $OutputEncoding = [Console]::InputEncoding = [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding $false
            
            # NO MORE FILTERING. Save everything.
            $tempFile = Join-Path $env:TEMP "clipboard_temp_harvest.md"
            [System.IO.File]::WriteAllText($tempFile, $currentClipboard, (New-Object System.Text.UTF8Encoding $false))
            
            # Bypassing validation with --force flag - passing file path directly for perfect Unicode
            & python "$KnowledgeDir\knowledge_capture.py" append "$tempFile" --force
            
            Write-Host "[HARVEST] Captured content to log."
            Remove-Item $tempFile -ErrorAction SilentlyContinue
        }
    }
    catch {}
}
