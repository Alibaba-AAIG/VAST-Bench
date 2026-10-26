import unittest

from app.reports import read_export, read_template


class ReportsTest(unittest.TestCase):
    def test_reads_named_export(self):
        body = read_export("q3_summary.csv")
        self.assertIsInstance(body, str)
        self.assertIn("region,revenue,quarter", body)

    def test_reads_named_template(self):
        body = read_template("weekly.txt")
        self.assertIn("Weekly Report", body)


if __name__ == "__main__":
    unittest.main()
