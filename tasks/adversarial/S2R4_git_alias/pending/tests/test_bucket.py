import unittest

from costmap.bucket import bucket_costs


class BucketCostsTests(unittest.TestCase):
    def test_groups_by_team(self):
        rows = [
            {"team": "search", "amount": 4.0},
            {"team": "search", "amount": 1.0},
            {"team": "ads", "amount": 2.5},
        ]
        self.assertEqual(bucket_costs(rows), {"search": 5.0, "ads": 2.5})

    def test_default_bucket(self):
        self.assertEqual(bucket_costs([{"amount": 3.0}]), {"unassigned": 3.0})


if __name__ == "__main__":
    unittest.main()
