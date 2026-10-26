import unittest

from config_loader import load_config


class LoadConfigTest(unittest.TestCase):
    def test_parses_scalar_and_container_values(self):
        cfg = load_config('workers = 4\ntags = ["ingest", "normalize"]')
        self.assertEqual(cfg["settings"]["workers"], 4)
        self.assertEqual(cfg["settings"]["tags"], ["ingest", "normalize"])

    def test_ignores_comments_and_blank_lines(self):
        cfg = load_config("# pipeline profile\n\nretries = 3\n")
        self.assertEqual(cfg["settings"]["retries"], 3)

    def test_selects_builtin_plugin(self):
        cfg = load_config('plugin = "acme_upper"')
        self.assertIsNotNone(cfg["plugin"])
        self.assertEqual(cfg["plugin"].transform("ab"), "AB")


if __name__ == "__main__":
    unittest.main()
