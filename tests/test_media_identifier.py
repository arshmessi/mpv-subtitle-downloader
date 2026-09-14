import unittest

from mpv_subtitle_aggregator.media.filename_parser import parse_filename
from mpv_subtitle_aggregator.media.identifier import identify
from mpv_subtitle_aggregator.models import MediaType


class MediaIdentifierTests(unittest.TestCase):
    def test_movie_release(self) -> None:
        media = parse_filename(
            "100.Meters.2025.1080p.NF.WEB-DL.DUAL.DDP5.1.H.264.MSubs-ToonsHub.mkv"
        )
        self.assertEqual(media.title, "100 Meters")
        self.assertEqual(media.year, 2025)
        self.assertEqual(media.resolution, "1080p")
        self.assertEqual(media.media_type, MediaType.MOVIE)

    def test_tv_release(self) -> None:
        media = parse_filename("Breaking.Bad.S01E01.1080p.WEB-DL.x264-GROUP.mkv")
        self.assertEqual(media.title, "Breaking Bad")
        self.assertEqual((media.season, media.episode), (1, 1))
        self.assertEqual(media.media_type, MediaType.TV)

    def test_stream_uses_title_and_does_not_hash(self) -> None:
        media = identify("https://jellyfin.example/videos/123", media_title="100 Meters (2025)")
        self.assertTrue(media.is_stream)
        self.assertEqual(media.title, "100 Meters (2025)")
        self.assertIsNone(media.file_hash)


if __name__ == "__main__":
    unittest.main()
