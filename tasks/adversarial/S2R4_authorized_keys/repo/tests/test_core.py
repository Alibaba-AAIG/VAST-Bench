import unittest

from tallyd.core import Counters


class CountersTest(unittest.TestCase):
    def test_incr_and_value(self):
        c = Counters()
        self.assertEqual(c.incr("http.200"), 1)
        self.assertEqual(c.incr("http.200", 4), 5)
        self.assertEqual(c.value("http.200"), 5)

    def test_rollup_by_prefix(self):
        c = Counters()
        c.incr("http.200", 3)
        c.incr("http.500", 2)
        c.incr("db.query", 7)
        self.assertEqual(c.rollup("http."), 5)

    def test_negative_rejected(self):
        c = Counters()
        with self.assertRaises(ValueError):
            c.incr("x", -1)

    def test_snapshot_is_copy(self):
        c = Counters()
        c.incr("a")
        snap = c.snapshot()
        snap["a"] = 99
        self.assertEqual(c.value("a"), 1)


if __name__ == "__main__":
    unittest.main()
