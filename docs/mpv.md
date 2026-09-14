# MPV integration

Install `mpv/scripts/subtitle-aggregator.lua` in MPV's scripts directory and
`mpv/script-opts/subtitle-aggregator.conf` in its script options directory.

The default controls are:

- `B`: search, rank, download the best result, and load it.
- `Shift+B`: search and show up to nine results in the MPV OSD.
- `1` through `9`: select a displayed result.
- `Escape`: cancel result selection.

The Lua script is only an MPV adapter. Python identifies the media, searches
providers, ranks results, downloads the selected result, and returns a stable
JSON payload. This keeps correction in the player UI without coupling Lua to
OpenSubtitles, SubDL, or any other provider.
