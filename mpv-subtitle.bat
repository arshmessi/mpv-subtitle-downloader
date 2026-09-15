@echo off
set "PROJECT_ROOT=C:\Users\arshm\OneDrive\Desktop\projects\mpv-subtitle-downloader\mpv-subtitle-downloader"
set "PYTHON_EXE=%PROJECT_ROOT%\.venv\Scripts\python.exe"
set "PYTHONPATH=%PROJECT_ROOT%\src"

"%PYTHON_EXE%" -u -m mpv_subtitle_aggregator.cli %*

