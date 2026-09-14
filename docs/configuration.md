# Configuration

Copy `config/config.example.toml` to `%APPDATA%\mpv-subtitle-aggregator\config.toml`.
Enable or disable providers under `[providers.<id>]`. Profiles select the
providers used by normal searches:

```toml
[profiles.default]
providers = ["embedded", "opensubtitles", "subdl"]
```

Set `profile = "default"` to select that profile. One-off CLI selection is
available with `--providers opensubtitles,subdl` or `--providers all`.

The `embedded` provider is local and uses FFmpeg's `ffprobe` and `ffmpeg`; it
does not require credentials. OpenSubtitles reads `OPEN_SUBTITLES_API_KEY`.
Never place credentials in this tracked example file.

The MPV options file belongs in MPV's `script-opts` directory. The Lua adapter
does not inspect subtitle contents, rendering settings, Anime4K, or Jellyfin
Shim configuration.
