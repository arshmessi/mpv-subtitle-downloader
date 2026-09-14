"""Credential-free movie search for SubDL's public website."""

from __future__ import annotations

import asyncio
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, urljoin
from urllib.request import Request, urlopen

from ..models import MediaInfo, MediaType, ProviderStatus, SubtitleResult
from .base import ProviderCapabilities, ProviderSearchResult, SubtitleProvider


class SubDLPublicProvider(SubtitleProvider):
    id = "subdl_public"
    name = "SubDL (public)"
    capabilities = ProviderCapabilities(movies=True, tv=False, title_search=True, languages=("en",))
    base_url = "https://subdl.com"

    async def search(self, media: MediaInfo, languages: list[str]) -> ProviderSearchResult:
        if media.media_type == MediaType.TV or media.season is not None:
            return ProviderSearchResult(
                message="public SubDL adapter currently supports movies only",
                status=ProviderStatus.UNSUPPORTED,
            )
        try:
            search_html = await asyncio.to_thread(self._get, f"/search/{quote(media.title)}")
            title_url = _find_title_url(search_html, media.title, media.year)
            if not title_url:
                return ProviderSearchResult(
                    message="no public SubDL movie page matched", status=ProviderStatus.NO_RESULTS
                )
            page_html = await asyncio.to_thread(self._get, title_url.rstrip("/") + "/english")
            rows = _parse_downloads(page_html)
        except TimeoutError:
            return ProviderSearchResult(
                message="SubDL request timed out", status=ProviderStatus.TIMEOUT
            )
        except OSError as error:
            return ProviderSearchResult(message=str(error), status=ProviderStatus.NETWORK_ERROR)
        results = [
            SubtitleResult(
                result_id=f"{self.id}-{index}",
                provider=self.id,
                language="en",
                release=release,
                downloadable=True,
                download_url=urljoin(self.base_url, download_url),
                raw_provider_data={"source": "subdl_public"},
            )
            for index, (release, download_url) in enumerate(rows, 1)
        ]
        return ProviderSearchResult(
            results,
            None if results else "no public English SubDL subtitles matched",
            ProviderStatus.SUCCESS if results else ProviderStatus.NO_RESULTS,
        )

    async def download(self, subtitle: SubtitleResult, destination: Path) -> Path:
        from ..download.downloader import download_file

        return await download_file(subtitle, destination)

    def _get(self, path: str) -> str:
        request = Request(
            urljoin(self.base_url, path),
            headers={"User-Agent": "mpv-subtitle-aggregator/0.1.0"},
        )
        with urlopen(request, timeout=15) as response:  # noqa: S310 - fixed public provider URL
            return response.read().decode("utf-8", errors="replace")


class _LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self.current_href: str | None = None
        self.current_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            self.current_href = dict(attrs).get("href")
            self.current_text = []

    def handle_data(self, data: str) -> None:
        if self.current_href is not None:
            self.current_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self.current_href:
            text = re.sub(r"\s+", " ", "".join(self.current_text)).strip()
            self.links.append((text, self.current_href))
            self.current_href = None


def _find_title_url(document: str, title: str, year: int | None) -> str | None:
    parser = _LinkParser()
    parser.feed(document)
    normalized = re.sub(r"[^a-z0-9]", "", title.lower())
    for text, href in parser.links:
        if "/subtitle/" not in href or "/s/" in href:
            continue
        haystack = re.sub(r"[^a-z0-9]", "", text.lower())
        if normalized in haystack and (year is None or str(year) in text):
            return href
    return None


def _parse_downloads(document: str) -> list[tuple[str, str]]:
    parser = _LinkParser()
    parser.feed(document)
    rows: list[tuple[str, str]] = []
    release = ""
    for text, href in parser.links:
        if "/s/info/" in href and text:
            release = text
        if "dl.subdl.com/" in href and href.lower().endswith(".zip"):
            rows.append((release or text or "SubDL English subtitle", href))
    return rows
