import asyncio
import unittest

from mpv_subtitle_aggregator.models import MediaInfo, MediaType, ProviderStatus
from mpv_subtitle_aggregator.providers.tvsubtitles import (
    TVSubtitlesProvider,
    _episode_rows,
    _extract_archive_path,
    _find_show_id,
)


class TVSubtitlesProviderTests(unittest.TestCase):
    def test_extracts_archive_path_from_download_interstitial(self) -> None:
        page = "var s1= 'fil'; var s2= 'es/T'; var s3= 'he'; var s4= ' Show.zip';"
        self.assertEqual(_extract_archive_path(page), "files/The Show.zip")

    def test_finds_series_and_exact_episode(self) -> None:
        catalog = '<a href="tvshow-231-1.html"><b>The Mentalist</b></a>'
        season = (
            '<td><a href="episode-1.html"><b>Wrong</b></a></td><td>'
            '<a href="subtitle-10.html"><img alt="en"></a></td>'
        )
        episode = '<title>TVsubtitles - The Mentalist 1x07</title>'
        provider = TVSubtitlesProvider()
        documents = {
            "tvshows.html": catalog,
            "tvshow-231-1.html": season,
            "episode-1.html": episode,
        }
        provider._get = lambda path: documents[path]
        response = asyncio.run(
            provider.search(
                MediaInfo("The Mentalist", media_type=MediaType.TV, season=1, episode=7),
                ["en"],
            )
        )
        self.assertEqual(response.status, ProviderStatus.SUCCESS)
        self.assertEqual(response.results[0].download_url, "https://www.tvsubtitles.net/download-10.html")

    def test_parser_rejects_other_episode_links(self) -> None:
        rows = _episode_rows(
            '<td><a href="episode-1.html"><b>Wrong</b></a></td><td>'
            '<a href="subtitle-10.html"><img alt="en"></a></td>'
        )
        self.assertEqual(rows[0][0], "episode-1.html")
        self.assertEqual(
            _find_show_id(
                '<a href="tvshow-231-1.html"><b>The Mentalist</b></a>', "The Mentalist"
            ),
            "231",
        )


if __name__ == "__main__":
    unittest.main()