$ErrorActionPreference = 'Stop'
$Root = Join-Path $env:LOCALAPPDATA 'mpv-subtitle-aggregator'
$Venv = Join-Path $Root '.venv'
New-Item -ItemType Directory -Force -Path $Root | Out-Null
py -3.11 -m venv $Venv
& (Join-Path $Venv 'Scripts\python.exe') -m pip install --upgrade pip
& (Join-Path $Venv 'Scripts\python.exe') -m pip install .
Write-Output "Installed isolated backend at $Root"
& (Join-Path $Venv 'Scripts\mpv-subtitle.exe') doctor