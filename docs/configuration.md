# Configuration

Copy `config/config.example.toml` to `%APPDATA%\mpv-subtitle-aggregator\config.toml`.
Enable or disable providers under `[providers.<id>]`. One-off CLI selection is
available with `--providers opensubtitles,subdl` or `--providers all`.

The MPV options file belongs in MPV's `script-opts` directory. The Lua adapter
does not inspect subtitle contents, rendering settings, Anime4K, or Jellyfin
Shim configuration.