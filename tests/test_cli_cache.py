import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from mpv_subtitle_aggregator.cli import _save_search_response
from mpv_subtitle_aggregator.models import MediaInfo, SearchResponse, SubtitleResult


class CliCacheTests(unittest.TestCase):
    def test_search_response_cache_preserves_result_ids(self) -> None:
        response = SearchResponse(
            True, MediaInfo("Film"), [SubtitleResult("r1", "opensubtitles", "en")]
        )
        with tempfile.TemporaryDirectory() as directory:
            with patch.dict(os.environ, {"LOCALAPPDATA": directory}):
                _save_search_response(response)
                cached = json.loads(
                    Path(directory, "mpv-subtitle-aggregator", "last-search.json").read_text()
                )
        self.assertEqual(cached["results"][0]["result_id"], "r1")


if __name__ == "__main__":
    unittest.main()