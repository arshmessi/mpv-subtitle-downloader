# Changelog

## [Unreleased]

### Added

- Embedded local subtitle discovery and FFmpeg extraction.
- MPV/Jellyfin installation, support, troubleshooting, ranking, release, and
    limitations documentation.

### Changed

- Default provider profile now checks embedded tracks before network providers.
- Provider profiles and configured priorities are applied by the loader.
- README and provider documentation now distinguish verified functionality from
    endpoint-dependent adapters.

## [0.1.0] - 2026-09-14

### Added

- Modular media identification, provider registry, concurrent search, ranking,
  selection, validation, CLI, MPV adapter, tests, and GitHub Actions workflows.