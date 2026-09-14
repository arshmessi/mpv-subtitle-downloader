"""Provider interface. Provider implementations never leak into the core."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..models import MediaInfo, ProviderStatus, SubtitleResult


@dataclass(frozen=True, slots=True)
class ProviderCapabilities:
    movies: bool = True
    tv: bool = True
    anime: bool = False
    hash_search: bool = False
    title_search: bool = True
    imdb_search: bool = False
    tmdb_search: bool = False
    languages: tuple[str, ...] = ()


@dataclass(slots=True)
class ProviderSearchResult:
    results: list[SubtitleResult] = field(default_factory=list)
    message: str | None = None
    status: ProviderStatus = ProviderStatus.SUCCESS


class SubtitleProvider(ABC):
    id: str
    name: str
    capabilities = ProviderCapabilities()

    @abstractmethod
    async def search(self, media: MediaInfo, languages: list[str]) -> ProviderSearchResult:
        """Return normalized results or raise a provider-specific error."""

    async def download(self, subtitle: SubtitleResult, destination: Path) -> Path:
        raise NotImplementedError(f"{self.id} does not implement downloads")

    def diagnostics(self) -> dict[str, Any]:
        return {"id": self.id, "name": self.name, "capabilities": self.capabilities}
