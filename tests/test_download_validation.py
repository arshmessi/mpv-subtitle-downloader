import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from mpv_subtitle_aggregator.download.downloader import _read_url
from mpv_subtitle_aggregator.download.validation import validate_subtitle


class DownloadValidationTests(unittest.TestCase):
    def test_download_request_accepts_provider_headers(self) -> None:
        captured = {}

        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return b"subtitle"

        def fake_urlopen(request, timeout):
            captured["url"] = request.full_url
            captured["headers"] = dict(request.headers)
            return Response()

        with patch("mpv_subtitle_aggregator.download.downloader.urlopen", fake_urlopen):
            _read_url("https://example.test/subtitle", {"Api-Key": "test-key"})

        self.assertEqual(captured["url"], "https://example.test/subtitle")
        self.assertEqual(captured["headers"]["Api-key"], "test-key")

    def test_rejects_html_error_page(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "error.srt"
            path.write_text("<html>access denied</html>", encoding="utf-8")
            with self.assertRaises(ValueError):
                validate_subtitle(path)

    def test_rejects_javascript_download_interstitial(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "interstitial.srt"
            path.write_text(
                "<script>document.location = 'files/subtitle.zip'</script>", encoding="utf-8"
            )
            with self.assertRaises(ValueError):
                validate_subtitle(path)

    def test_accepts_srt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "subtitle.srt"
            path.write_text("1\n00:00:01,000 --> 00:00:02,000\nHello\n", encoding="utf-8")
            validate_subtitle(path)


if __name__ == "__main__":
    unittest.main()
