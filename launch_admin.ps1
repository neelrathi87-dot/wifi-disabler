# Désactivateur - Lanceur avec élévation automatique
# Double-cliquez sur ce fichier pour lancer le serveur en Administrateur

$ErrorActionPreference = "Stop"

# ── Self-elevate if not already admin ───────────────────────
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    $psArgs = "-NoExit -ExecutionPolicy Bypass -File `"$PSCommandPath`""
    Start-Process powershell -Verb RunAs -ArgumentList $psArgs
    exit
}

# ── Already admin from here ──────────────────────────────────
$py     = "C:\Users\neeln\AppData\Local\Programs\Python\Python312\python.exe"
$script = "c:\Users\neeln\wifi disabler\server.py"

Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "  Désactivateur  ·  http://localhost:5000" -ForegroundColor Cyan
Write-Host "  Statut : Administrateur ✓" -ForegroundColor Green
Write-Host "=======================================================" -ForegroundColor Cyan

# Open browser after 1.5s
Start-Job { Start-Sleep 1.5; Start-Process "http://localhost:5000" } | Out-Null

# Start server
& $py $script
