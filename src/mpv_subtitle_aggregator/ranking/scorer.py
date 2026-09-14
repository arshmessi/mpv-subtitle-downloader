"""Transparent recommendation scoring; selection remains a separate concern."""

from __future__ import annotations

import re

from ..models import MediaInfo, SubtitleResult


def score_result(media: MediaInfo, result: SubtitleResult, language: str = "en") -> float:
    score = 0.0
    if result.language.lower() == language.lower():
        score += 35
    if result.content_hash and media.file_hash and result.content_hash == media.file_hash:
        score += 40
    release = result.release.lower()
    if media.year and str(media.year) in release:
        score += 8
    if media.resolution and media.resolution.lower() in release:
        score += 5
    if media.source and _compact(media.source) in _compact(release):
        score += 6
    if media.media_type.value == "tv" and media.season is not None and f"s{media.season:02d}" in release:
        score += 3
    if media.media_type.value == "tv" and media.episode is not None and f"e{media.episode:02d}" in release:
        score += 3
    if not result.hearing_impaired:
        score += 2
    if not result.forced:
        score += 1
    return min(score, 100.0)


def rank_results(media: MediaInfo, results: list[SubtitleResult], language: str = "en") -> list[SubtitleResult]:
    for result in results:
        result.score = score_result(media, result, language)
    return sorted(results, key=lambda result: result.score, reverse=True)


def _compact(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())