import tempfile
import unittest
from pathlib import Path

from mpv_subtitle_aggregator.config import load_config


class ConfigTests(unittest.TestCase):
    def test_profile_and_priority_are_applied(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.toml"
            path.write_text(
                """
profile = "fast"

[providers.subdl]
enabled = true
priority = 20

[providers.embedded]
enabled = true
priority = 200

[profiles.fast]
providers = ["embedded", "subdl"]
""",
                encoding="utf-8",
            )
            config = load_config(path)
        self.assertEqual(config.profile, "fast")
        self.assertEqual(config.providers, ["embedded", "subdl"])


if __name__ == "__main__":
    unittest.main()