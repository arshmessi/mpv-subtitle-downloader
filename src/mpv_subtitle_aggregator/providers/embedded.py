"""Local embedded subtitle tracks exposed through ffprobe/ffmpeg."""

from __future__ import annotations

import asyncio
import json
import subprocess
from pathlib import Path

from ..models import MediaInfo, SubtitleResult
from .base import ProviderCapabilities, ProviderSearchResult, SubtitleProvider


class EmbeddedSubtitleProvider(SubtitleProvider):
    id = "embedded"
    name = "Embedded subtitles"
    capabilities = ProviderCapabilities(languages=())

    async def search(self, media: MediaInfo, languages: list[str]) -> ProviderSearchResult:
        if media.is_stream or not media.path:
            return ProviderSearchResult(message="embedded subtitles require a local media file")
        try:
            tracks = await asyncio.to_thread(_probe_subtitles, Path(media.path))
        except FileNotFoundError:
            return ProviderSearchResult(message="ffprobe is not installed or not available on PATH")
        except (OSError, subprocess.CalledProcessError, json.JSONDecodeError) as error:
            return ProviderSearchResult(message=f"embedded subtitle inspection failed: {error}")
        results: list[SubtitleResult] = []
        for position, track in enumerate(tracks, 1):
            language = str(track.get("language") or "und").lower()
            if languages and language != "und" and language not in languages:
                continue
            title = str(track.get("title") or f"Track {position}")
            results.append(
                SubtitleResult(
                    result_id=f"embedded-{track['index']}",
                    provider=self.id,
                    language=language,
                    release=title,
                    hearing_impaired=bool(track.get("hearing_impaired")),
                    forced=bool(track.get("forced")),
                    raw_provider_data={"path": media.path, "stream_index": track["index"]},
                )
            )
        message = None if results else "no matching embedded subtitle tracks"
        return ProviderSearchResult(results, message)

    async def download(self, subtitle: SubtitleResult, destination: Path) -> Path:
        source = Path(str(subtitle.raw_provider_data["path"]))
        stream_index = int(subtitle.raw_provider_data["stream_index"])
        destination.mkdir(parents=True, exist_ok=True)
        output = destination / f"{subtitle.result_id}.srt"
        await asyncio.to_thread(_extract_subtitle, source, stream_index, output)
        from ..download.validation import validate_subtitle

        validate_subtitle(output)
        return output


def _probe_subtitles(path: Path) -> list[dict[str, object]]:
    completed = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "s",
            "-show_entries",
            "stream=index:stream_tags=language,title:stream_disposition=forced,hearing_impaired",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)
    tracks = []
    for stream in payload.get("streams", []):
        tags = stream.get("tags", {})
        disposition = stream.get("disposition", {})
        tracks.append(
            {
                "index": stream["index"],
                "language": tags.get("language"),
                "title": tags.get("title"),
                "forced": disposition.get("forced", 0),
                "hearing_impaired": disposition.get("hearing_impaired", 0),
            }
        )
    return tracks


def _extract_subtitle(source: Path, stream_index: int, output: Path) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            str(source),
            "-map",
            f"0:{stream_index}",
            "-c:s",
            "srt",
            str(output),
        ],
        check=True,
        capture_output=True,
        text=True,
    )