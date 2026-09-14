# MPV Subtitle Aggregator

Manual subtitle search and download tooling for MPV and Jellyfin MPV Shim.

The project keeps MPV integration, media identification, provider adapters,
ranking, selection, and downloading independent. MPV continues to own embedded
subtitle tracks; this tool searches and adds external subtitles only when the
user explicitly invokes it.

## Status

Version 0.1.0 is a core/developer preview. Movie/TV filename identification,
provider orchestration, ranking, selection, safe downloads, and MPV integration
are implemented. The default credential-free provider is a public SubDL movie
adapter. OpenSubtitles.com, SubDL API, and SubSource API adapters remain
optional and require the user's own configuration.

## What works now

| Capability                                 | Status                                    |
| ------------------------------------------ | ----------------------------------------- |
| Local movie and TV filename identification | Available                                 |
| MPV/Jellyfin metadata identification       | Available; HTTP is never hashed           |
| MPV-owned embedded subtitle handling       | Aggregator does not inspect or replace it |
| Manual alternative result selection        | Available                                 |
| Manual media-title correction              | Available                                 |
| Credential-free provider                   | SubDL public movie pages                  |
| OpenSubtitles.com                          | Optional API key                          |
| SubDL/SubSource APIs                       | Optional endpoint/API configuration       |
| Automatic/background subtitle search       | Not implemented by design                 |

## Quick start

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
mpv-subtitle providers
mpv-subtitle search-title "100 Meters" --year 2025 --language en --json
```

See [docs/installation.md](docs/installation.md), [docs/configuration.md](docs/configuration.md),
[docs/jellyfin.md](docs/jellyfin.md), [docs/troubleshooting.md](docs/troubleshooting.md),
and [docs/architecture.md](docs/architecture.md).

Live OpenSubtitles checks are opt-in and require `OPEN_SUBTITLES_API_KEY`; normal
CI never contacts providers.

## Privacy and network behavior

The video itself is not uploaded. Enabled providers receive identification data
such as title, year, episode, and, where configured, a local media hash. HTTP
stream URLs are never hashed. Review provider terms before enabling a provider.

## License

GPL-3.0-or-later. See [LICENSE](LICENSE).
