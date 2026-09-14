$ErrorActionPreference = 'Stop'
$Root = Join-Path $env:LOCALAPPDATA 'mpv-subtitle-aggregator'
if (Test-Path $Root) { Remove-Item -Recurse -Force $Root }
Write-Output "Removed $Root"