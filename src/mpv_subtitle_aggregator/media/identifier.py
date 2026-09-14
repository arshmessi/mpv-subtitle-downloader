"""Build MediaInfo from local paths or MPV metadata."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

from .filename_parser import parse_filename
from ..models import MediaInfo, MediaType


def identify(
    path: str | None = None,
    *,
    filename: str | None = None,
    media_title: str | None = None,
    metadata: dict[str, object] | None = None,
) -> MediaInfo:
    """Identify media without requiring MPV or any provider dependency."""
    metadata = metadata or {}
    source_name = filename or (Path(path).name if path and not _is_url(path) else None)
    parsed = parse_filename(source_name) if source_name else MediaInfo(title=media_title or "")
    if media_title and (not source_name or parsed.title == parsed.filename):
        parsed.title = _clean_title(media_title)
    parsed.path = path
    parsed.is_stream = bool(path and _is_url(path))
    parsed.mpv_title = media_title
    parsed.duration = _number(metadata.get("duration"))
    parsed.width = _integer(metadata.get("width"))
    parsed.height = _integer(metadata.get("height"))
    parsed.fps = _number(metadata.get("fps") or metadata.get("container-fps"))
    parsed.file_size = _integer(metadata.get("file-size"))
    parsed.raw_metadata = metadata
    if parsed.resolution is None and parsed.height:
        parsed.resolution = f"{parsed.height}p"
    if parsed.media_type == MediaType.UNKNOWN and parsed.season is not None:
        parsed.media_type = MediaType.TV
    if not parsed.title:
        raise ValueError("MEDIA_IDENTITY_UNKNOWN: no meaningful media title was provided")
    return parsed


def identify_json(payload: str) -> MediaInfo:
    """Identify media from a JSON MPV request payload."""
    return identify(**json.loads(payload))


def _is_url(value: str) -> bool:
    return urlparse(value).scheme in {"http", "https", "rtmp", "rtsp"}


def _number(value: object) -> float | None:
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _integer(value: object) -> int | None:
    number = _number(value)
    return int(number) if number is not None else None


def _clean_title(value: str) -> str:
    return value.strip().replace("\n", " ")