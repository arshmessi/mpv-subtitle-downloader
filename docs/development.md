# Development

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest
ruff check .
```

Live provider tests are intentionally excluded from CI. Set provider endpoint
configuration and add explicit opt-in tests before running them. OpenSubtitles
can be tested against its real API without downloading a subtitle:

```powershell
$env:OPEN_SUBTITLES_API_KEY = "enter it directly in this terminal"
$env:MPV_SUBTITLE_LIVE_TESTS = "1"
python -m pytest tests/test_live_opensubtitles.py -v
Remove-Item Env:OPEN_SUBTITLES_API_KEY,Env:MPV_SUBTITLE_LIVE_TESTS
```

For GitHub, create an Actions secret named `OPEN_SUBTITLES_API_KEY` and run the
manual `Live provider test` workflow. Never put the key in a file, command-line
argument, commit, issue, or chat message. The repository does not contain video
files, downloaded subtitles, credentials, or local config.