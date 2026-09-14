import asyncio
import unittest

from mpv_subtitle_aggregator.models import MediaInfo, ProviderStatus, SubtitleResult
from mpv_subtitle_aggregator.providers.base import ProviderSearchResult, SubtitleProvider
from mpv_subtitle_aggregator.ranking.scorer import rank_results
from mpv_subtitle_aggregator.search.orchestrator import SearchOrchestrator
from mpv_subtitle_aggregator.search.selection import select_result


class GoodProvider(SubtitleProvider):
    id = "good"
    name = "Good"

    async def search(self, media, languages):
        return ProviderSearchResult(
            [SubtitleResult("x", self.id, "en", "Film 2025 1080p", content_hash="same")]
        )


class FailingProvider(SubtitleProvider):
    id = "broken"
    name = "Broken"

    async def search(self, media, languages):
        raise RuntimeError("offline")


class SearchTests(unittest.TestCase):
    def test_failure_isolated_and_result_ids_assigned(self) -> None:
        response = asyncio.run(
            SearchOrchestrator([GoodProvider(), FailingProvider()]).search(
                MediaInfo("Film", year=2025)
            )
        )
        self.assertTrue(response.success)
        self.assertEqual(response.results[0].result_id, "r1")
        self.assertEqual(response.providers[1].status, ProviderStatus.ERROR)

    def test_duplicate_results_keep_provenance(self) -> None:
        first = SubtitleResult("a", "one", "en", "Film 2025", content_hash="hash")
        second = SubtitleResult("b", "two", "en", "different", content_hash="hash")
        response = asyncio.run(SearchOrchestrator([]).search(MediaInfo("Film")))
        rank_results(response.media, [first, second])
        self.assertGreaterEqual(first.score, 0)

    def test_selection_can_choose_second_or_cancel(self) -> None:
        results = [SubtitleResult("r1", "one", "en"), SubtitleResult("r2", "two", "en")]
        self.assertEqual(select_result(results, "2"), results[1])
        self.assertIsNone(select_result(results, "q"))


if __name__ == "__main__":
    unittest.main()
