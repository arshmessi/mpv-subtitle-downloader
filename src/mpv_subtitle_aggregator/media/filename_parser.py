"""Conservative filename parsing independent of MPV and providers."""

from __future__ import annotations

import re
from pathlib import Path

from ..models import MediaInfo, MediaType

_TV_RE = re.compile(r"(?:^|[. _-])S(?P<season>\d{1,2})E(?P<episode>\d{1,3})(?:$|[. _-])", re.I)
_YEAR_RE = re.compile(r"(?<!\d)(19\d{2}|20\d{2})(?!\d)")
_RESOLUTION_RE = re.compile(r"(?P<value>\d{3,4}p|\d{3,4}x\d{3,4})", re.I)
_SOURCE_RE = re.compile(r"\b(WEB[- .]?DL|WEB[- .]?Rip|Blu[- .]?Ray|HDTV|DVD[- .]?Rip)\b", re.I)
_CODEC_RE = re.compile(r"\b(x264|x265|h\.?264|h\.?265|hevc|av1)\b", re.I)
_GROUP_RE = re.compile(r"[- ](?P<group>[A-Za-z][A-Za-z0-9]+)(?:\[[^]]+\])?$")
_NOISE_RE = re.compile(
    r"\b(?:2160p|1080p|720p|480p|WEB[- .]?DL|WEB[- .]?Rip|Blu[- .]?Ray|HDTV|"
    r"DDP?(?:\d\.\d)?|AAC\d?(?:\.\d)?|DUAL|REMUX|PROPER|REPACK|x264|x265|"
    r"h\.?(?:264|265)|HEVC|AV1|MULTI|SUBBED|DUBBED)\b",
    re.I,
)


def parse_filename(filename: str) -> MediaInfo:
    """Parse common movie, TV, and anime release naming conventions."""
    name = Path(filename).name
    stem = Path(name).stem
    tv_match = _TV_RE.search(stem.replace("[", " ").replace("]", " "))
    year_match = _YEAR_RE.search(stem)
    resolution_match = _RESOLUTION_RE.search(stem)
    source_match = _SOURCE_RE.search(stem)
    codec_match = _CODEC_RE.search(stem)
    group_match = _GROUP_RE.search(stem.replace(".", " "))

    media_type = MediaType.TV if tv_match else MediaType.MOVIE
    title_end = tv_match.start() if tv_match else (year_match.start() if year_match else len(stem))
    title = stem[:title_end]
    title = re.sub(r"[._]+", " ", title)
    title = re.sub(r"\[[^]]*\]", " ", title)
    title = re.sub(r"\s+", " ", title).strip(" -")
    title = _NOISE_RE.sub(" ", title)
    title = re.sub(r"\s+", " ", title).strip(" -") or stem

    resolution = resolution_match.group("value") if resolution_match else None
    if resolution and "x" in resolution.lower():
        resolution = f"{resolution.split('x', 1)[1]}p"

    source = source_match.group(1).replace(".", " ").replace("-", "-").upper() if source_match else None
    return MediaInfo(
        title=title,
        year=int(year_match.group(1)) if year_match else None,
        media_type=media_type,
        season=int(tv_match.group("season")) if tv_match else None,
        episode=int(tv_match.group("episode")) if tv_match else None,
        filename=name,
        resolution=resolution,
        source=source,
        release_group=group_match.group("group") if group_match else None,
        video_codec=codec_match.group(1).upper() if codec_match else None,
    )