"""Reproduction for bug #4821 — parser.parse_header raises on a malformed header.

Plain unittest.TestCase (no pytest fixtures), so it runs under any standard runner:
    python -m unittest incoming.repro_tests.test_parser
    pytest incoming/repro_tests
"""
import os
import sys
import unittest

# Make the project's parser importable regardless of how the suite is invoked.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from parser import MalformedHeaderError, parse_header


class MalformedHeaderReproTest(unittest.TestCase):
    def test_missing_colon_raises(self):
        # Header line with no ':' separator — this is the crash the report is about.
        with self.assertRaises(MalformedHeaderError):
            parse_header("Content-Length 42")

    def test_wellformed_header_ok(self):
        self.assertEqual(parse_header("Content-Length: 42"), ("Content-Length", "42"))


if __name__ == "__main__":
    unittest.main()
