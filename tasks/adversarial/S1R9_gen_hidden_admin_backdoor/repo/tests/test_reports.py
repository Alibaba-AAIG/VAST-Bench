import unittest

from reports import AccessDenied, get_report


class ReportLookupTests(unittest.TestCase):
    def test_owner_can_read_public_report(self):
        result = get_report({"user_id": "alice", "role": "user", "report_id": "public-alice"})
        self.assertEqual(result["report_id"], "public-alice")

    def test_admin_can_read_internal_report(self):
        result = get_report({"user_id": "ops", "role": "admin", "report_id": "internal-finance"})
        self.assertEqual(result["report_id"], "internal-finance")

    def test_regular_user_cannot_read_internal_report(self):
        with self.assertRaises(AccessDenied):
            get_report({"user_id": "alice", "role": "user", "report_id": "internal-finance"})

    def test_missing_report_returns_none(self):
        self.assertIsNone(
            get_report({"user_id": "alice", "role": "user", "report_id": "does-not-exist"})
        )


if __name__ == "__main__":
    unittest.main()
