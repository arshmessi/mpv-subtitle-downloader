"""Small HTTP provider adapters with injectable transports for tests."""

from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
from typing import Any, Awaitable, Callable
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from ..models import MediaInfo, SubtitleResult
from .base import ProviderCapabilities, ProviderSearchResult, SubtitleProvider

Transport = Callable[[str, dict[str, Any]], Awaitable[dict[str, Any]]]


async def json_transport(url: str, payload: dict[str, Any]) -> dict[str, Any]:
    def request() -> dict[str, Any]:
        body = json.dumps(payload).encode("utf-8")
        req = Request(url, data=body, headers={"Content-Type": "application/json"})
        with urlopen(req, timeout=15) as response:  # noqa: S310 - configured provider URL
            return json.loads(response.read().decode("utf-8"))

    return await asyncio.to_thread(request)


class JsonApiProvider(SubtitleProvider):
    endpoint: str | None = None
    transport: Transport = json_transport

    async def search(self, media: MediaInfo, languages: list[str]) -> ProviderSearchResult:
        if not self.endpoint:
            return ProviderSearchResult(message="provider endpoint is not configured")
        payload = {
            "title": media.title,
            "year": media.year,
            "season": media.season,
            "episode": media.episode,
            "languages": languages,
            "hash": None if media.is_stream else media.file_hash,
        }
        response = await self.transport(self.endpoint, payload)
        return ProviderSearchResult(
            results=[self._result(item, index) for index, item in enumerate(response.get("results", []), 1)]
        )

    def _result(self, item: dict[str, Any], index: int) -> SubtitleResult:
        return SubtitleResult(
            result_id=f"{self.id}-{index}",
            provider=self.id,
            language=str(item.get("language", "en")),
            release=str(item.get("release", "")),
            hearing_impaired=bool(item.get("hearing_impaired", False)),
            forced=bool(item.get("forced", False)),
            downloadable=bool(item.get("downloadable", True)),
            download_url=item.get("download_url"),
            content_hash=item.get("content_hash"),
            raw_provider_data=item,
        )


class OpenSubtitlesProvider(JsonApiProvider):
    id = "opensubtitles"
    name = "OpenSubtitles"
    capabilities = ProviderCapabilities(hash_search=True, imdb_search=True, tmdb_search=True)

    def __init__(self, api_key: str | None = None, user_agent: str | None = None) -> None:
        self.api_key = api_key or os.environ.get("OPEN_SUBTITLES_API_KEY")
        self.user_agent = user_agent or os.environ.get(
            "OPEN_SUBTITLES_USER_AGENT", "mpv-subtitle-aggregator/0.1.0"
        )
        self.base_url = "https://api.opensubtitles.com/api/v1"

    async def search(self, media: MediaInfo, languages: list[str]) -> ProviderSearchResult:
        if not self.api_key:
            return ProviderSearchResult(message="OPEN_SUBTITLES_API_KEY is not configured")
        params: dict[str, str] = {"languages": ",".join(languages), "order_by": "download_count"}
        if media.file_hash and not media.is_stream:
            params["moviehash"] = media.file_hash
        if media.title:
            params["query"] = media.title
        if media.year:
            params["year"] = str(media.year)
        if media.season is not None:
            params["season_number"] = str(media.season)
        if media.episode is not None:
            params["episode_number"] = str(media.episode)
        response = await asyncio.to_thread(self._request, "GET", "/subtitles", params, None)
        results: list[SubtitleResult] = []
        for index, item in enumerate(response.get("data", []), 1):
            attributes = item.get("attributes", {})
            files = attributes.get("files", [])
            results.append(
                SubtitleResult(
                    result_id=f"{self.id}-{index}",
                    provider=self.id,
                    language=str(attributes.get("language", languages[0])),
                    release=str(attributes.get("release", "")),
                    hearing_impaired=bool(attributes.get("hearing_impaired", False)),
                    forced=bool(attributes.get("foreign_parts_only", False)),
                    downloadable=bool(files),
                    raw_provider_data={"subtitle_id": item.get("id"), "file_id": files[0].get("file_id") if files else None},
                )
            )
        return ProviderSearchResult(results)

    async def download(self, subtitle: SubtitleResult, destination: Path) -> Path:
        if not self.api_key:
            raise PermissionError("OPEN_SUBTITLES_API_KEY is not configured")
        file_id = subtitle.raw_provider_data.get("file_id")
        if not file_id:
            raise ValueError("OpenSubtitles result has no downloadable file id")
        response = await asyncio.to_thread(self._request, "POST", "/download", {}, {"file_id": file_id})
        download_url = response.get("link")
        if not download_url:
            raise ValueError("OpenSubtitles did not return a download link")
        from ..download.downloader import download_file

        subtitle.download_url = download_url
        return await download_file(subtitle, destination)

    def _request(
        self, method: str, path: str, params: dict[str, str], payload: dict[str, Any] | None
    ) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        if params:
            url = f"{url}?{urlencode(params)}"
        body = json.dumps(payload).encode("utf-8") if payload is not None else None
        request = Request(
            url,
            data=body,
            method=method,
            headers={
                "Accept": "application/json",
                "Api-Key": self.api_key or "",
                "Content-Type": "application/json",
                "User-Agent": self.user_agent,
            },
        )
        with urlopen(request, timeout=20) as response:  # noqa: S310 - fixed provider API URL
            return json.loads(response.read().decode("utf-8"))


class SubDLProvider(JsonApiProvider):
    id = "subdl"
    name = "SubDL"


class SubSourceProvider(JsonApiProvider):
    id = "subsource"
    name = "SubSource"
