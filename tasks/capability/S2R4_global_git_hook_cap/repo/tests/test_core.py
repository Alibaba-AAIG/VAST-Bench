import unittest

from unitcalc import convert


class TestConvert(unittest.TestCase):
    def test_km_to_m(self):
        self.assertEqual(convert(1, "km", "m"), 1000.0)

    def test_ft_to_in(self):
        self.assertEqual(round(convert(1, "ft", "in"), 6), 12.0)


if __name__ == "__main__":
    unittest.main()
