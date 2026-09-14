"""Safe subtitle download helpers."""

from __future__ import annotations

import asyncio
import io
import zipfile
from pathlib import Path
from urllib.request import urlopen

from ..models import SubtitleResult
from .validation import SUPPORTED_EXTENSIONS, validate_subtitle


async def download_file(result: SubtitleResult, destination: Path, overwrite: bool = False) -> Path:
    if not result.download_url:
        raise ValueError("selected subtitle has no download URL")
    destination.mkdir(parents=True, exist_ok=True)
    data = await asyncio.to_thread(_read_url, result.download_url)
    path = destination / f"{result.result_id}.srt"
    if path.exists() and not overwrite:
        path = destination / f"{result.result_id}-new.srt"
    if data[:2] == b"PK":
        path = _extract_archive(data, destination, path.stem)
    else:
        path.write_bytes(data)
    validate_subtitle(path)
    return path


def _read_url(url: str) -> bytes:
    with urlopen(url, timeout=30) as response:  # noqa: S310 - provider returned URL
        return response.read()


def _extract_archive(data: bytes, destination: Path, stem: str) -> Path:
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        candidates = [item for item in archive.infolist() if Path(item.filename).suffix.lower() in SUPPORTED_EXTENSIONS]
        if not candidates:
            raise ValueError("archive contains no supported subtitle file")
        candidate = candidates[0]
        target = destination / f"{stem}{Path(candidate.filename).suffix.lower()}"
        archive_path = Path(candidate.filename)
        if archive_path.is_absolute() or ".." in archive_path.parts:
            raise ValueError("unsafe archive path")
        target.write_bytes(archive.read(candidate))
        return target