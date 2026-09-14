# Configuration

Copy `config/config.example.toml` to `%APPDATA%\mpv-subtitle-aggregator\config.toml`.
Profiles choose the providers used by normal searches:

```toml
profile = "default"

[profiles.default]
providers = ["subdl_public", "opensubtitles", "subdl"]
```

The `subdl_public` provider searches public movie pages and downloads public
English SRT archives without credentials. OpenSubtitles reads
`OPEN_SUBTITLES_API_KEY`. Never place credentials in this tracked example file.

One-off CLI selection is available with `--providers opensubtitles,subdl` or
`--providers all`. The MPV options file belongs in MPV's `script-opts` directory.
The Lua adapter does not inspect embedded subtitle contents or modify rendering,
Anime4K, shaders, mpv_ext, or Jellyfin Shim configuration.
