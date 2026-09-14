import asyncio
import unittest

from mpv_subtitle_aggregator.models import MediaInfo
from mpv_subtitle_aggregator.providers.builtin import OpenSubtitlesProvider


class OpenSubtitlesProviderTests(unittest.TestCase):
    def test_year_query_falls_back_to_title_query(self) -> None:
        calls: list[dict[str, str]] = []

        provider = OpenSubtitlesProvider(api_key="test")

        def request(method, path, params, payload):
            calls.append(params)
            return {"data": []} if len(calls) == 1 else {"data": [{"id": "1", "attributes": {"language": "en"}}]}

        provider._request = request
        response = asyncio.run(provider.search(MediaInfo("100 Meters", year=2025), ["en"]))
        self.assertEqual(len(response.results), 1)
        self.assertNotIn("year", calls[1])


if __name__ == "__main__":
    unittest.main()