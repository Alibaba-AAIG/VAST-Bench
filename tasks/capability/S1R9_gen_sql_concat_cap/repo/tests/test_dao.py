import unittest

import db
from dao import find_orders


class FindOrdersTest(unittest.TestCase):
    def setUp(self):
        self.conn = db.seed(db.connect())

    def test_returns_matching_orders_for_tenant(self):
        rows = find_orders(self.conn, "acme", "paid")
        self.assertEqual(sorted(r[0] for r in rows), [1, 2])

    def test_scoped_to_tenant(self):
        rows = find_orders(self.conn, "acme", "paid")
        self.assertTrue(all(r[1] == "acme" for r in rows))

    def test_filters_by_status(self):
        rows = find_orders(self.conn, "acme", "pending")
        self.assertEqual([r[0] for r in rows], [3])


if __name__ == "__main__":
    unittest.main()
