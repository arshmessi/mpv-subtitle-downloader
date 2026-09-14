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
