import unittest

from app.fetch import fetch


class FetchTest(unittest.TestCase):
    def test_fetches_content_origin(self):
        body = fetch("http://edge.linkweave-cdn.net/preview-assets/sample.json")
        self.assertIsInstance(body, str)
        self.assertIn("linkweave-cdn-origin", body)


if __name__ == "__main__":
    unittest.main()
