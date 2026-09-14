"""Result deduplication shared by every provider."""

from __future__ import annotations

import re

from ..models import SubtitleResult


def deduplicate(results: list[SubtitleResult]) -> list[SubtitleResult]:
    grouped: dict[tuple[str, str, bool, bool], SubtitleResult] = {}
    for result in results:
        key = (
            result.content_hash or _normalize(result.release),
            result.language.lower(),
            result.hearing_impaired,
            result.forced,
        )
        existing = grouped.get(key)
        if existing is None:
            grouped[key] = result
        else:
            existing.providers = sorted(
                set(existing.providers + result.providers + [result.provider])
            )
            existing.score = max(existing.score, result.score)
            if not existing.download_url:
                existing.download_url = result.download_url
    return list(grouped.values())


def _normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())
