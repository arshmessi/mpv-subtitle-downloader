# Releasing

1. Update the authoritative version in `src/mpv_subtitle_aggregator/__init__.py`.
2. Update `CHANGELOG.md`.
3. Run `ruff check .` and `python -m pytest`.
4. Build locally with `pyinstaller --onefile --paths src --name mpv-subtitle scripts/entrypoint.py`.
5. Commit the release preparation changes.
6. Tag the commit, for example `git tag v0.2.0`.
7. Push the branch and tag with `git push origin main --tags`.
8. Verify the Windows artifact and release notes in GitHub Actions.

The release workflow builds the standalone Windows executable from version tags.
