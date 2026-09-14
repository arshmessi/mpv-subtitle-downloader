import asyncio
import os
import unittest
from unittest.mock import patch

from mpv_subtitle_aggregator.models import MediaInfo, ProviderStatus
from mpv_subtitle_aggregator.providers.builtin import OpenSubtitlesProvider


class OpenSubtitlesProviderTests(unittest.TestCase):
    def test_missing_api_key_is_not_configured(self) -> None:
        with patch.dict(os.environ, {"OPEN_SUBTITLES_API_KEY": ""}):
            response = asyncio.run(
                OpenSubtitlesProvider(api_key=None).search(MediaInfo("Film"), ["en"])
            )
        self.assertEqual(response.status, ProviderStatus.NOT_CONFIGURED)

    def test_imdb_id_is_sent_without_tt_prefix(self) -> None:
        captured: dict[str, str] = {}
        provider = OpenSubtitlesProvider(api_key="test")

        def request(method, path, params, payload):
            captured.update(params)
            return {"data": []}

        provider._request = request
        asyncio.run(
            provider.search(MediaInfo("100 Meters", year=2025, imdb_id="tt32600395"), ["en"])
        )
        self.assertEqual(captured["imdb_id"], "32600395")
        self.assertNotIn("query", captured)

    def test_year_query_falls_back_to_title_query(self) -> None:
        calls: list[dict[str, str]] = []

        provider = OpenSubtitlesProvider(api_key="test")

        def request(method, path, params, payload):
            calls.append(params)
            return (
                {"data": []}
                if len(calls) == 1
                else {"data": [{"id": "1", "attributes": {"language": "en"}}]}
            )

        provider._request = request
        response = asyncio.run(provider.search(MediaInfo("100 Meters", year=2025), ["en"]))
        self.assertEqual(len(response.results), 1)
        self.assertNotIn("year", calls[1])


if __name__ == "__main__":
    unittest.main()
