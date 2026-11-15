import json
import tempfile
import unittest
from pathlib import Path

from src.refresh import load_config


class ConfigTest(unittest.TestCase):
    def test_retry_limit_default(self):
        config = json.loads(Path("config/service.json").read_text(encoding="utf-8"))
        self.assertEqual(config["retry_limit"], 3)


if __name__ == "__main__":
    unittest.main()
