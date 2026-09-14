import asyncio
import os
import unittest

from mpv_subtitle_aggregator.models import MediaInfo
from mpv_subtitle_aggregator.providers.builtin import OpenSubtitlesProvider


@unittest.skipUnless(
    os.environ.get("MPV_SUBTITLE_LIVE_TESTS") == "1"
    and os.environ.get("OPEN_SUBTITLES_API_KEY"),
    "set MPV_SUBTITLE_LIVE_TESTS=1 and OPEN_SUBTITLES_API_KEY to run live tests",
)
class OpenSubtitlesLiveTests(unittest.TestCase):
    def test_known_title_search(self) -> None:
        response = asyncio.run(
            OpenSubtitlesProvider().search(MediaInfo("100 Meters", year=2025), ["en"])
        )
        self.assertIsInstance(response.results, list)
        self.assertTrue(response.results, response.message or "OpenSubtitles returned no results")


if __name__ == "__main__":
    unittest.main()