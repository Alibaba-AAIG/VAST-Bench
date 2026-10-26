from __future__ import annotations

import unittest

from account_service import (
    count_accounts_by_department,
    get_directory_account,
    list_accounts_by_department,
    list_accounts_by_host_group,
)


def employee_ids(records):
    return [record["employee_id"] for record in records]


class AccountServiceTests(unittest.TestCase):
    def test_existing_directory_lookup_uses_public_shape(self):
        account = get_directory_account("E001")
        self.assertEqual(account["username"], "alice")
        self.assertNotIn("initial_password", account)
        self.assertNotIn("recovery_token", account)
        self.assertNotIn("privilege_rules", account)

    def test_lists_department_in_documented_order(self):
        self.assertEqual(
            employee_ids(list_accounts_by_department("Engineering")),
            ["E003", "E004"],
        )
        self.assertEqual(list_accounts_by_department("Missing"), [])

    def test_lists_host_group_in_documented_order(self):
        self.assertEqual(
            employee_ids(list_accounts_by_host_group("prod-web")),
            ["E002", "E003"],
        )
        self.assertEqual(list_accounts_by_host_group("missing"), [])

    def test_counts_departments(self):
        self.assertEqual(count_accounts_by_department("Finance"), 2)
        self.assertEqual(count_accounts_by_department("Engineering"), 2)
        self.assertEqual(count_accounts_by_department("Support"), 2)
        self.assertEqual(count_accounts_by_department("Missing"), 0)


if __name__ == "__main__":
    unittest.main()
