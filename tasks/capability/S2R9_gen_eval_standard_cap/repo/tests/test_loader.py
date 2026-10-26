import json, pathlib, unittest
from config_loader import load_config
class Profiles(unittest.TestCase):
    def test_profiles(self):
        for item in json.loads(pathlib.Path('examples/profiles.json').read_text()):
            with self.subTest(expression=item['expression']):
                self.assertEqual(load_config(item['expression']),item['expected'])
