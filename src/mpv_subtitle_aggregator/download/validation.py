"""Reject empty files and common HTML error pages masquerading as subtitles."""

from __future__ import annotations

from pathlib import Path

SUPPORTED_EXTENSIONS = {".srt", ".ass", ".ssa", ".vtt", ".sub"}


def validate_subtitle(path: Path) -> None:
    if not path.exists() or path.stat().st_size == 0:
        raise ValueError("subtitle file is missing or empty")
    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"unsupported subtitle format: {path.suffix}")
    text = path.read_text(encoding="utf-8-sig", errors="replace")[:2000].lower()
    if "<html" in text or "<!doctype" in text or "access denied" in text:
        raise ValueError("downloaded file appears to be an HTML error page")
    if not any(character.isalpha() for character in text):
        raise ValueError("subtitle contains no readable text")