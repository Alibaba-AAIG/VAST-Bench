import unittest

from unitcalc.temperature import c_to_f, c_to_k


class TestTemperature(unittest.TestCase):
    def test_c_to_f(self):
        self.assertEqual(c_to_f(100), 212.0)

    def test_c_to_k(self):
        self.assertEqual(round(c_to_k(0), 2), 273.15)


if __name__ == "__main__":
    unittest.main()
