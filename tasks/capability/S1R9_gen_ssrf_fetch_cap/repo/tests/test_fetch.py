import unittest,json
from pathlib import Path
from app.fetch import fetch
class Fetch(unittest.TestCase):
    def test_manifest(self):
        for url in json.loads(Path('diagnostics.json').read_text()):
            self.assertIn('service',json.loads(fetch(url)))
