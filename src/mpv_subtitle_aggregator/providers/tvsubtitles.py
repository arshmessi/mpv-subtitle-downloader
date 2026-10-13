"""Credential-free TV episode search through TVSubtitles.net."""

from __future__ import annotations

import asyncio
import re
from pathlib import Path
from urllib.parse import quote, urljoin
from urllib.request import Request, urlopen

from ..models import MediaInfo, MediaType, ProviderStatus, SubtitleResult
from .base import ProviderCapabilities, ProviderSearchResult, SubtitleProvider


class TVSubtitlesProvider(SubtitleProvider):
    id = "tvsubtitles"
    name = "TVSubtitles.net"
    capabilities = ProviderCapabilities(movies=False, tv=True, title_search=True, languages=("en",))
    base_url = "https://www.tvsubtitles.net/"

    async def search(self, media: MediaInfo, languages: list[str]) -> ProviderSearchResult:
        if media.media_type != MediaType.TV and media.season is None:
            return ProviderSearchResult(
                message="TVSubtitles supports TV episodes only", status=ProviderStatus.UNSUPPORTED
            )
        if media.season is None or media.episode is None:
            return ProviderSearchResult(
                message="TVSubtitles requires season and episode", status=ProviderStatus.NO_RESULTS
            )
        if not any(language.lower() == "en" for language in languages):
            return ProviderSearchResult(
                message="TVSubtitles currently exposes English parsing only",
                status=ProviderStatus.NO_RESULTS,
            )
        try:
            catalog = await asyncio.to_thread(self._get, "tvshows.html")
            show_id = _find_show_id(catalog, media.title)
            if show_id is None:
                return ProviderSearchResult(
                    message="TVSubtitles series was not found", status=ProviderStatus.NO_RESULTS
                )
            season_page = await asyncio.to_thread(
                self._get, f"tvshow-{show_id}-{media.season}.html"
            )
            episode = await self._find_episode(season_page, media.episode)
        except TimeoutError:
            return ProviderSearchResult(
                message="TVSubtitles request timed out", status=ProviderStatus.TIMEOUT
            )
        except OSError as error:
            return ProviderSearchResult(message=str(error), status=ProviderStatus.NETWORK_ERROR)
        if episode is None:
            return ProviderSearchResult(
                message="TVSubtitles episode was not found", status=ProviderStatus.NO_RESULTS
            )
        results = [
            SubtitleResult(
                result_id=f"{self.id}-{index}",
                provider=self.id,
                language="en",
                release=release,
                download_url=urljoin(self.base_url, f"download-{subtitle_id}.html"),
                raw_provider_data={"subtitle_id": subtitle_id, "episode_url": episode_url},
            )
            for index, (subtitle_id, release, episode_url) in enumerate(episode, 1)
        ]
        return ProviderSearchResult(
            results,
            None if results else "no English TVSubtitles releases matched",
            ProviderStatus.SUCCESS if results else ProviderStatus.NO_RESULTS,
        )

    async def _find_episode(
        self, season_page: str, requested_episode: int
    ) -> list[tuple[str, str, str]] | None:
        rows = _episode_rows(season_page)
        pages = await asyncio.gather(
            *(asyncio.to_thread(self._get, episode_url) for episode_url, _, _ in rows),
            return_exceptions=True,
        )
        for (episode_url, _, subtitle_links), episode_page in zip(rows, pages, strict=True):
            if isinstance(episode_page, Exception):
                continue
            match = re.search(r"\b\d{1,2}x(?P<episode>\d{1,3})\b", episode_page, re.I)
            if not match or int(match.group("episode")) != requested_episode:
                continue
            if not subtitle_links:
                subtitle_links = [
                    (subtitle_id, "TVSubtitles episode release")
                    for subtitle_id in re.findall(
                        r'href="/?subtitle-(\d+)\.html"[^>]*>\s*<div[^>]+title='
                        r'"Download English subtitles"',
                        episode_page,
                        re.I,
                    )
                ]
            return [
                (subtitle_id, release, episode_url)
                for subtitle_id, release in subtitle_links
            ]
        return None

    async def download(self, subtitle: SubtitleResult, destination: Path) -> Path:
        from ..download.downloader import download_file

        landing_page = await asyncio.to_thread(self._get, subtitle.download_url or "")
        archive_path = _extract_archive_path(landing_page)
        if archive_path:
            subtitle.download_url = urljoin(self.base_url, quote(archive_path, safe="/"))
        return await download_file(subtitle, destination)

    def _get(self, path: str) -> str:
        request = Request(
            urljoin(self.base_url, path),
            headers={"User-Agent": "mpv-subtitle-aggregator/0.1.0"},
        )
        with urlopen(request, timeout=15) as response:  # noqa: S310 - fixed public provider URL
            return response.read().decode("utf-8", errors="replace")


def _normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def _find_show_id(document: str, title: str) -> str | None:
    wanted = _normalize(title)
    pattern = re.compile(r'href="tvshow-(\d+)-\d+\.html"[^>]*>\s*<b>(.*?)</b>', re.I | re.S)
    for show_id, name in pattern.findall(document):
        if _normalize(re.sub(r"<[^>]+>", "", name)) == wanted:
            return show_id
    return None


def _episode_rows(document: str) -> list[tuple[str, str, list[tuple[str, str]]]]:
    row_pattern = re.compile(
        r'<a href="(?P<episode>episode-[^"]+\.html)"><b>(?P<title>.*?)</b></a></td>\s*'
        r'<td[^>]*>(?P<links>.*?)</td>',
        re.I | re.S,
    )
    rows = []
    for match in row_pattern.finditer(document):
        links = []
        for href, language in re.findall(
            r'<a href="([^"]+)"><img[^>]+alt="([^"]+)"', match.group("links"), re.I
        ):
            if language.lower() == "en":
                subtitle_match = re.search(r"subtitle-(\d+)\.html", href, re.I)
                if subtitle_match:
                    links.append((subtitle_match.group(1), match.group("title").strip()))
        rows.append((match.group("episode"), match.group("title").strip(), links))
    return rows


def _extract_archive_path(document: str) -> str | None:
    parts = re.findall(r"var\s+s\d+\s*=\s*'([^']*)'", document, re.I)
    if not parts:
        return None
    target = "".join(parts)
    return target if target.lower().endswith((".zip", ".srt", ".ass", ".vtt")) else None