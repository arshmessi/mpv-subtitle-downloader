import asyncio
import os
import unittest

from mpv_subtitle_aggregator.models import MediaInfo, ProviderStatus
from mpv_subtitle_aggregator.providers.subdl_public import SubDLPublicProvider


@unittest.skipUnless(
    os.environ.get("MPV_SUBTITLE_LIVE_TESTS") == "1",
    "set MPV_SUBTITLE_LIVE_TESTS=1 to run the live public-provider test",
)
class SubDLPublicLiveTests(unittest.TestCase):
    def test_known_movie_search(self) -> None:
        response = asyncio.run(
            SubDLPublicProvider().search(MediaInfo("100 Meters", year=2025), ["en"])
        )
        self.assertEqual(response.status, ProviderStatus.SUCCESS)
        self.assertTrue(response.results)


if __name__ == "__main__":
    unittest.main()