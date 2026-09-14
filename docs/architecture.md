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