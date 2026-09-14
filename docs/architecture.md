# Architecture

The system has seven independent boundaries:

1. MPV Lua gathers properties and starts the backend.
2. `media.identifier` turns filenames and metadata into `MediaInfo`.
3. The search orchestrator runs enabled providers concurrently.
4. Providers implement `SubtitleProvider` and return normalized results.
5. Ranking recommends results but never removes alternatives.
6. Selection chooses a result or cancels.
7. Downloading validates files and safely extracts archives.

Provider errors are reported per provider and cannot discard successful results.
HTTP streams are identified from metadata and are never hashed.

## Identification and correction

For local media, the Python filename parser identifies common release tokens:
title, year, `SxxEyy`, resolution, source, codec, and release group. For HTTP
or Jellyfin streams, the MPV adapter forwards `media-title` and other safe MPV
properties; the backend does not hash the URL. Provider results are ranked as a
recommendation, never treated as unquestionable truth.

The MPV Lua adapter owns correction at the player boundary. `B` opens one
navigable subtitle menu. The menu can run a quick best-match search, show ranked
results in the MPV OSD with keys `1` through `9`, or correct the media title
before searching again. Escape cancels active menus/selections, and the chosen
file is loaded with `sub-add`. The Lua layer does not parse titles or provider
responses beyond the stable JSON contract.
