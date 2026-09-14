# Jellyfin MPV Shim

For Jellyfin MPV Shim HTTP streams, the application uses MPV metadata such as
`media-title`, filename, duration, and dimensions. It does not hash an HTTP
stream and never treats the URL as the title.

The flow is:

```text
Jellyfin metadata -> MPV properties -> Lua adapter -> Python MediaInfo -> title search
```

Downloaded subtitles are stored in the configured local cache and loaded into
MPV with `sub-add`; they are not written beside the remote HTTP URL. Embedded
subtitle inspection applies only to local media files. Anime4K, shaders, GPU
settings, and Jellyfin rendering settings are outside this project's scope.

If identity is wrong, open the subtitle menu with the configured hotkey and
choose **Correct media title and search**.
