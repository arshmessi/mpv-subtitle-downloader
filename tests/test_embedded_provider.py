import asyncio
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from mpv_subtitle_aggregator.models import MediaInfo, SubtitleResult
from mpv_subtitle_aggregator.providers.embedded import EmbeddedSubtitleProvider


class EmbeddedProviderTests(unittest.TestCase):
    def test_discovers_matching_embedded_language(self) -> None:
        probe = {
            "streams": [
                {
                    "index": 3,
                    "tags": {"language": "eng", "title": "English"},
                    "disposition": {"forced": 0, "hearing_impaired": 1},
                },
                {"index": 4, "tags": {"language": "spa"}, "disposition": {}},
            ]
        }
        completed = type("Result", (), {"stdout": json.dumps(probe)})()
        with patch("subprocess.run", return_value=completed):
            response = asyncio.run(
                EmbeddedSubtitleProvider().search(
                    MediaInfo("Film", path="film.mkv"), ["eng"]
                )
            )
        self.assertEqual(len(response.results), 1)
        self.assertTrue(response.results[0].hearing_impaired)
        self.assertEqual(response.results[0].raw_provider_data["stream_index"], 3)

    def test_streams_do_not_use_embedded_provider(self) -> None:
        response = asyncio.run(
            EmbeddedSubtitleProvider().search(
                MediaInfo("Film", path="https://example.test/video", is_stream=True), ["eng"]
            )
        )
        self.assertFalse(response.results)

    def test_extracts_embedded_track(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            source = destination / "film.mkv"
            source.write_bytes(b"video")
            completed = type("Result", (), {"stdout": ""})()

            def fake_ffmpeg(command, **kwargs):
                Path(command[-1]).write_text(
                    "1\n00:00:01,000 --> 00:00:02,000\nHello\n", encoding="utf-8"
                )
                return completed

            with patch("subprocess.run", side_effect=fake_ffmpeg) as run:
                output = asyncio.run(
                    EmbeddedSubtitleProvider().download(
                        SubtitleResult(
                            "embedded-3",
                            "embedded",
                            "eng",
                            raw_provider_data={"path": str(source), "stream_index": 3},
                        ),
                        destination,
                    )
                )
            self.assertEqual(output.suffix, ".srt")
            self.assertEqual(run.call_args.args[0][0], "ffmpeg")


if __name__ == "__main__":
    unittest.main()