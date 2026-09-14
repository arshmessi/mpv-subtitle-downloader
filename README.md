# MPV Subtitle Aggregator

Modular subtitle search and download tooling for MPV and Jellyfin MPV Shim.

The project keeps MPV integration, media identification, provider adapters,
ranking, selection, and downloading independent. It is designed to work well
with local files and metadata-only HTTP streams.

## Status

Version 0.1.0 is the initial usable core: filename identification, provider
contracts and registry, concurrent search orchestration, ranking, safe subtitle
download/validation, CLI commands, and MPV integration are included. Provider
network adapters require the relevant credentials or endpoint configuration.

## Quick start

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
mpv-subtitle providers
mpv-subtitle search-title "100 Meters" --year 2025 --language en --json
```

See [docs/development.md](docs/development.md), [docs/configuration.md](docs/configuration.md),
and [docs/architecture.md](docs/architecture.md) for setup and extension details.

Live OpenSubtitles checks are opt-in and require `OPEN_SUBTITLES_API_KEY`; the
normal CI suite never contacts providers.

## License

GPL-3.0-or-later. See [LICENSE](LICENSE).

