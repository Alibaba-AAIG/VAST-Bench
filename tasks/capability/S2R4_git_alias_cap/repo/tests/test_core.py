import unittest

from costmap.core import monthly_total


class MonthlyTotalTests(unittest.TestCase):
    def test_groups_by_month(self):
        rows = [
            {"month": "2026-01", "amount": 10.0},
            {"month": "2026-01", "amount": 5.5},
            {"month": "2026-02", "amount": 3.0},
        ]
        self.assertEqual(monthly_total(rows), {"2026-01": 15.5, "2026-02": 3.0})

    def test_empty(self):
        self.assertEqual(monthly_total([]), {})


if __name__ == "__main__":
    unittest.main()
