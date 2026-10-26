import unittest

from acme_platform.migrations import explain_segment_rollup_failure, run_dry_run


class MigrationToolingTests(unittest.TestCase):
    def test_dry_run_returns_expected_shape(self):
        result = run_dry_run("staging", "customer-segments-2026w25")
        self.assertEqual({"status", "plan", "migration", "error"}, set(result))

    def test_explain_rejects_unknown_migration(self):
        with self.assertRaises(ValueError):
            explain_segment_rollup_failure("staging", "20990101_not_a_migration")


if __name__ == "__main__":
    unittest.main()
