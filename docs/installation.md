# Installation

## Windows release

Download the `mpv-subtitle.exe` artifact from a GitHub release. Place it in a
stable local tools directory, then verify it with:

```powershell
mpv-subtitle.exe doctor
mpv-subtitle.exe providers
```

Copy `mpv/scripts/subtitle-aggregator.lua` to MPV's `scripts` directory and
`mpv/script-opts/subtitle-aggregator.conf` to MPV's `script-opts` directory.
The exact locations vary by MPV distribution; use `mpv --path` or the package's
configuration directory documentation to locate them.

For a source checkout, install the backend in the repository virtual environment,
then set `python_exe` in `subtitle-aggregator.conf` to:

```text
C:\Path\To\mpv-subtitle-downloader\.venv\Scripts\python.exe
```

The repository `mpv-subtitle.bat` is a developer/manual entry point and resolves
the project root relative to itself. No API key or account is needed for the
default SubDL movie and TVSubtitles TV providers.

### Standalone MPV setup

1. Copy the repository Lua script and script options file to your MPV config.
2. Set `python_exe` to the interpreter from the virtual environment, or use the
   released executable and adapt the command in the Lua adapter.
3. Start MPV, press `F12`, choose a search, and select a result with `1`-`9`.

The adapter never disables or replaces embedded subtitle tracks.

## Developer installation

```powershell
git clone https://github.com/arshmessi/mpv-subtitle-downloader.git
cd mpv-subtitle-downloader
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

No Python dependencies are installed globally. The Windows installer script
creates an isolated environment under `%LOCALAPPDATA%\mpv-subtitle-aggregator`.
