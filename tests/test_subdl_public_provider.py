import asyncio
import unittest

from mpv_subtitle_aggregator.models import MediaInfo, MediaType, ProviderStatus
from mpv_subtitle_aggregator.providers.subdl_public import (
    SubDLPublicProvider,
    _find_title_url,
    _parse_downloads,
)


class SubDLPublicProviderTests(unittest.TestCase):
    def test_parses_public_search_and_download_links(self) -> None:
        search_html = '<a href="/subtitle/sd1/100-meters">100 METERS (2025) movie</a>'
        page_html = (
            '<a href="/s/info/release/100-meters">WEB-DL release</a>'
            '<a href="https://dl.subdl.com/subtitle/1.zip">Quick Download</a>'
        )
        provider = SubDLPublicProvider()
        documents = {
            "/search/100%20Meters": search_html,
            "/subtitle/sd1/100-meters/english": page_html,
        }
        provider._get = lambda path: documents[path]
        response = asyncio.run(
            provider.search(MediaInfo("100 Meters", year=2025, media_type=MediaType.MOVIE), ["en"])
        )
        self.assertEqual(response.status, ProviderStatus.SUCCESS)
        self.assertEqual(response.results[0].download_url, "https://dl.subdl.com/subtitle/1.zip")
        self.assertEqual(response.results[0].release, "WEB-DL release")

    def test_tv_is_explicitly_unsupported_for_first_adapter(self) -> None:
        response = asyncio.run(
            SubDLPublicProvider().search(
                MediaInfo("Show", media_type=MediaType.TV, season=1, episode=1), ["en"]
            )
        )
        self.assertEqual(response.status, ProviderStatus.UNSUPPORTED)

    def test_parsers_handle_no_matches(self) -> None:
        self.assertIsNone(_find_title_url("<html></html>", "Film", 2025))
        self.assertEqual(_parse_downloads("<html></html>"), [])


if __name__ == "__main__":
    unittest.main()
