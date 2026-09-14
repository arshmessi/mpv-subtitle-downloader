"""Stable domain models shared by all layers."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class MediaType(StrEnum):
    MOVIE = "movie"
    TV = "tv"
    UNKNOWN = "unknown"


class ProviderStatus(StrEnum):
    SUCCESS = "success"
    NO_RESULTS = "no_results"
    NOT_CONFIGURED = "not_configured"
    AUTH_REQUIRED = "auth_required"
    RATE_LIMITED = "rate_limited"
    BLOCKED = "blocked"
    NETWORK_ERROR = "network_error"
    PARSER_ERROR = "parser_error"
    UNSUPPORTED = "unsupported"
    TIMEOUT = "timeout"
    OK = "ok"
    UNAVAILABLE = "unavailable"
    AUTHENTICATION_REQUIRED = "authentication_required"
    ERROR = "error"


@dataclass(slots=True)
class MediaInfo:
    title: str
    year: int | None = None
    media_type: MediaType = MediaType.UNKNOWN
    season: int | None = None
    episode: int | None = None
    filename: str | None = None
    path: str | None = None
    is_stream: bool = False
    imdb_id: str | None = None
    tmdb_id: str | None = None
    tvdb_id: str | None = None
    duration: float | None = None
    file_size: int | None = None
    file_hash: str | None = None
    width: int | None = None
    height: int | None = None
    fps: float | None = None
    resolution: str | None = None
    source: str | None = None
    edition: str | None = None
    release_group: str | None = None
    video_codec: str | None = None
    audio_codec: str | None = None
    mpv_title: str | None = None
    raw_metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class SubtitleResult:
    result_id: str
    provider: str
    language: str
    release: str = ""
    score: float = 0.0
    hearing_impaired: bool = False
    forced: bool = False
    downloadable: bool = True
    download_url: str | None = None
    content_hash: str | None = None
    providers: list[str] = field(default_factory=list)
    raw_provider_data: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.providers:
            self.providers = [self.provider]


@dataclass(slots=True)
class ProviderReport:
    provider: str
    status: ProviderStatus
    result_count: int = 0
    message: str | None = None


@dataclass(slots=True)
class SearchResponse:
    success: bool
    media: MediaInfo
    results: list[SubtitleResult] = field(default_factory=list)
    providers: list[ProviderReport] = field(default_factory=list)
    message: str | None = None
