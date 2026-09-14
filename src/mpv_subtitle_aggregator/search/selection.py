"""Interactive result selection that can be reused by CLI or MPV bridges."""

from __future__ import annotations

from collections.abc import Callable

from ..models import SubtitleResult


def select_result(
    results: list[SubtitleResult], choice: str | None = None, input_fn: Callable[[str], str] = input
) -> SubtitleResult | None:
    if not results:
        return None
    value = choice if choice is not None else input_fn("Select subtitle number, or q to cancel: ")
    if value.lower() in {"q", "quit", "cancel", "esc"}:
        return None
    try:
        index = int(value) - 1
        return results[index] if 0 <= index < len(results) else None
    except ValueError:
        return None
