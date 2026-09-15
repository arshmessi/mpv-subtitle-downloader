@echo off
set "PROJECT_ROOT=C:\Path\To\Your\Project"
set "PYTHON_EXE=%PROJECT_ROOT%\.venv\Scripts\python.exe"
set "PYTHONPATH=%PROJECT_ROOT%\src"

"%PYTHON_EXE%" -u -m mpv_subtitle_aggregator.cli %*
