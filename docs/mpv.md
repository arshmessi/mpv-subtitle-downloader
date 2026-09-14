# MPV integration

Install `mpv/scripts/subtitle-aggregator.lua` in MPV's scripts directory and
`mpv/script-opts/subtitle-aggregator.conf` in its script options directory.

The integration uses one global shortcut to avoid collisions with other MPV
scripts. The default control is:

- `B`: open the subtitle menu.

Navigate the menu with Up/Down, press Enter to choose, or Escape to close it:

- Quick search and load best match.
- Search and choose a subtitle, then select with `1` through `9`.
- Correct the media title and search again.

Result selection and title correction use temporary key bindings only while
their respective UI is open.

The Lua script is only an MPV adapter. Python identifies the media, searches
providers, ranks results, downloads the selected result, and returns a stable
JSON payload. This keeps correction in the player UI without coupling Lua to
OpenSubtitles, SubDL, or any other provider.
