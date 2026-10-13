@echo off
setlocal

set "PROJECT_ROOT=%~dp0"
set "PYTHON_EXE=%PROJECT_ROOT%\.venv\Scripts\python.exe"
set "PYTHONPATH=%PROJECT_ROOT%\src"

"%PYTHON_EXE%" -u -m mpv_subtitle_aggregator.cli %*

exit /b %ERRORLEVEL%