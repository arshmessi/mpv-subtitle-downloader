"""Provider registration and explicit enablement."""

from __future__ import annotations

from collections.abc import Iterable

from .base import SubtitleProvider
from .builtin import OpenSubtitlesProvider, SubDLProvider, SubSourceProvider
from .embedded import EmbeddedSubtitleProvider


class ProviderRegistry:
    def __init__(self, providers: Iterable[SubtitleProvider] = ()) -> None:
        self._providers = {provider.id: provider for provider in providers}

    def register(self, provider: SubtitleProvider) -> None:
        self._providers[provider.id] = provider

    def get(self, provider_id: str) -> SubtitleProvider:
        return self._providers[provider_id]

    def all(self) -> list[SubtitleProvider]:
        return list(self._providers.values())

    def select(
        self, include: list[str] | None = None, exclude: list[str] | None = None
    ) -> list[SubtitleProvider]:
        excluded = set(exclude or [])
        providers = (
            self.all()
            if include is None or "all" in include
            else [self.get(item) for item in include]
        )
        return [provider for provider in providers if provider.id not in excluded]


def built_in_registry() -> ProviderRegistry:
    return ProviderRegistry(
        [EmbeddedSubtitleProvider(), OpenSubtitlesProvider(), SubDLProvider(), SubSourceProvider()]
    )
