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

    def test_tv_release_with_compact_episode_number(self) -> None:
        media = parse_filename("The.Mentalist.1x07.HDTV.x264-GROUP.mkv")
        self.assertEqual(media.title, "The Mentalist")
        self.assertEqual((media.season, media.episode), (1, 7))
        self.assertEqual(media.media_type, MediaType.TV)

    def test_stream_uses_title_and_does_not_hash(self) -> None:
        media = identify("https://jellyfin.example/videos/123", media_title="100 Meters (2025)")
        self.assertTrue(media.is_stream)
        self.assertEqual(media.title, "100 Meters (2025)")
        self.assertIsNone(media.file_hash)

    def test_stream_media_title_preserves_tv_episode_identity(self) -> None:
        media = identify(
            "https://jellyfin.example/videos/123?MediaSourceId=x&api_key=y",
            media_title="The Mentalist - s1e13 - Paint It Red",
        )
        self.assertEqual(media.title, "The Mentalist")
        self.assertEqual((media.season, media.episode), (1, 13))
        self.assertEqual(media.media_type, MediaType.TV)
        self.assertTrue(media.is_stream)

    def test_explicit_title_overrides_wrong_filename_title(self) -> None:
        media = identify(
            "Wrong.Movie.2024.mkv",
            filename="Wrong.Movie.2024.mkv",
            media_title="Correct Movie",
        )
        self.assertEqual(media.title, "Correct Movie")


if __name__ == "__main__":
    unittest.main()
