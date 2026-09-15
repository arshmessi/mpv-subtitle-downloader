"""Concurrent provider search with isolated failures."""

from __future__ import annotations

import asyncio
import json
from collections.abc import Iterable

from ..models import MediaInfo, ProviderReport, ProviderStatus, SearchResponse, SubtitleResult
from ..providers.base import SubtitleProvider
from ..ranking.scorer import rank_results
from .normalization import deduplicate


class SearchOrchestrator:
    def __init__(
        self, providers: Iterable[SubtitleProvider], timeout: float = 15.0, max_concurrency: int = 8
    ) -> None:
        self.providers = list(providers)
        self.timeout = timeout
        self._semaphore = asyncio.Semaphore(max_concurrency)

    async def search(self, media: MediaInfo, languages: list[str] | None = None) -> SearchResponse:
        languages = languages or ["en"]
        
        # Primary search using original media info
        tasks = [self._search_provider(provider, media, languages) for provider in self.providers]
        collected = await asyncio.gather(*tasks)
        
        reports = [item[0] for item in collected]
        results = deduplicate(
            [result for _, provider_results in collected for result in provider_results]
        )
        
        # Fallback: if no results, try a cleaned title search
        if not results:
            from ..media.filename_parser import _NOISE_RE
            # Create a "cleaned" version of the media for the fallback search
            fallback_media = MediaInfo(
                title=_NOISE_RE.sub(" ", media.title).strip(),
                year=media.year,
                media_type=media.media_type,
                season=media.season,
                episode=media.episode
            )
            
            tasks = [self._search_provider(provider, fallback_media, languages) for provider in self.providers]
            collected = await asyncio.gather(*tasks)
            
            # Merge reports (overwrite failures with fallback results)
            for i, (_, provider_results) in enumerate(collected):
                if provider_results:
                    reports[i] = ProviderReport(
                        self.providers[i].id, ProviderStatus.SUCCESS, len(provider_results), None
                    )
                    results.extend(provider_results)
            
            results = deduplicate(results)

        rank_results(media, results, languages[0])
        for index, result in enumerate(results, 1):
            result.result_id = f"r{index}"
        return SearchResponse(
            bool(results),
            media,
            results,
            reports,
            None if results else "No suitable subtitles found",
        )

    async def _search_provider(
        self, provider: SubtitleProvider, media: MediaInfo, languages: list[str]
    ) -> tuple[ProviderReport, list[SubtitleResult]]:
        async with self._semaphore:
            try:
                response = await asyncio.wait_for(provider.search(media, languages), self.timeout)
                return ProviderReport(
                    provider.id, response.status, len(response.results), response.message
                ), response.results
            except TimeoutError:
                return ProviderReport(
                    provider.id, ProviderStatus.TIMEOUT, message="provider timed out"
                ), []
            except PermissionError as error:
                return ProviderReport(
                    provider.id, ProviderStatus.AUTH_REQUIRED, message=str(error)
                ), []
            except ConnectionError as error:
                return ProviderReport(
                    provider.id, ProviderStatus.NETWORK_ERROR, message=str(error)
                ), []
            except (json.JSONDecodeError, ValueError) as error:
                return ProviderReport(
                    provider.id, ProviderStatus.PARSER_ERROR, message=str(error)
                ), []
            except Exception as error:  # provider failures are intentionally isolated
                return ProviderReport(provider.id, ProviderStatus.ERROR, message=str(error)), []
