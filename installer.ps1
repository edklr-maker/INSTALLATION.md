# Installe l'agent de montage sur ce PC : FFmpeg, Python 3.12, environnement .venv et modele Whisper.
# Lancer en double-cliquant sur installer.bat (ou : powershell -ExecutionPolicy Bypass -File installer.ps1)
# Messages sans accents : PowerShell 5.1 lit mal les scripts UTF-8.
$ErrorActionPreference = "Stop"
$racine = $PSScriptRoot
Set-Location $racine

function Etape($texte) { Write-Host "`n== $texte" -ForegroundColor Cyan }

Etape "FFmpeg"
$ffmpeg = Get-Command ffmpeg -ErrorAction SilentlyContinue
if (-not $ffmpeg) {
    $ffmpeg = Get-ChildItem "$env:LOCALAPPDATA\Microsoft\WinGet\Packages\Gyan.FFmpeg*" -Filter ffmpeg.exe -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
}
if ($ffmpeg) { Write-Host "deja installe" }
else { winget install --id Gyan.FFmpeg -e --silent --accept-source-agreements --accept-package-agreements }

Etape "Python 3.12"
$python = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"
if (-not (Test-Path $python)) {
    winget install --id Python.Python.3.12 -e --silent --scope user --accept-source-agreements --accept-package-agreements
}
if (-not (Test-Path $python)) { throw "Python 3.12 introuvable dans $python" }
& $python --version

Etape "Environnement .venv"
if (-not (Test-Path "$racine\.venv\Scripts\python.exe")) { & $python -m venv "$racine\.venv" }
& "$racine\.venv\Scripts\python.exe" -m pip install --quiet --upgrade pip
& "$racine\.venv\Scripts\python.exe" -m pip install --quiet -r "$racine\requirements.txt"

Etape "Dossiers"
foreach ($d in "rushs", "rushs\traites", "montages", "travail") { New-Item -ItemType Directory -Force "$racine\$d" | Out-Null }

Etape "Modele Whisper (telechargement unique)"
$env:HF_HUB_DISABLE_SYMLINKS_WARNING = "1"
$modele = (Get-Content "$racine\config.json" -Raw | ConvertFrom-Json).modele_whisper
& "$racine\.venv\Scripts\python.exe" -c "from faster_whisper import WhisperModel; WhisperModel('$modele', device='cpu', compute_type='int8'); print('modele $modele pret')"

Write-Host "`nInstallation terminee dans $racine" -ForegroundColor Green
Write-Host "Etape suivante : ouvrir ce dossier dans Claude et demander de creer la tache du dimanche (voir INSTALLATION.md)."
