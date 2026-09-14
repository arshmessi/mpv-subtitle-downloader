# MPV Subtitle Aggregator

Modular subtitle search and download tooling for MPV and Jellyfin MPV Shim.

The project keeps MPV integration, media identification, provider adapters,
ranking, selection, and downloading independent. It is designed to work well
with local files and metadata-only HTTP streams.

## Status

Version 0.1.0 is a core/developer preview. Local filename identification,
embedded subtitle inspection, provider contracts, concurrent orchestration,
ranking, selection, safe download validation, CLI commands, and MPV integration
are implemented. The network adapters currently require provider-specific
credentials or endpoint configuration; unverified anonymous website scrapers
are deliberately not advertised as supported.

## What works now

| Capability                                        | Status                          |
| ------------------------------------------------- | ------------------------------- |
| Local movie and TV filename identification        | Available                       |
| Embedded local subtitle discovery                 | Available with FFmpeg           |
| HTTP/Jellyfin metadata identification             | Available; no HTTP hashing      |
| Alternative result selection and title correction | Available in MPV                |
| Concurrent provider failure isolation             | Available                       |
| OpenSubtitles API adapter                         | API key required                |
| SubDL and SubSource adapters                      | Endpoint configuration required |
| Credential-free internet providers                | Not yet verified                |

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
and [docs/architecture.md](docs/architecture.md) for setup and extension details.

Live OpenSubtitles checks are opt-in and require `OPEN_SUBTITLES_API_KEY`; the
normal CI suite never contacts providers.

## Privacy and network behavior

The video itself is not uploaded. When searching, the application sends
identification data to enabled providers, such as title, year, episode, and,
for eligible local files, a media hash. HTTP stream URLs are not hashed.
Review enabled providers and their terms before using the application.

## License

GPL-3.0-or-later. See [LICENSE](LICENSE).
