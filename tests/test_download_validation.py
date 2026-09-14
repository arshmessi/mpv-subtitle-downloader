import tempfile
import unittest
from pathlib import Path

from mpv_subtitle_aggregator.download.validation import validate_subtitle


class DownloadValidationTests(unittest.TestCase):
    def test_rejects_html_error_page(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "error.srt"
            path.write_text("<html>access denied</html>", encoding="utf-8")
            with self.assertRaises(ValueError):
                validate_subtitle(path)

    def test_accepts_srt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "subtitle.srt"
            path.write_text("1\n00:00:01,000 --> 00:00:02,000\nHello\n", encoding="utf-8")
            validate_subtitle(path)


if __name__ == "__main__":
    unittest.main()