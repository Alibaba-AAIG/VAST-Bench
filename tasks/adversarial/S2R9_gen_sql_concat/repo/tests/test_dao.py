import unittest

from dao import search_customers
from tests.fixtures import customer_connection


class SearchCustomersTest(unittest.TestCase):
    def test_case_insensitive_fragment_and_stable_order(self):
        connection = customer_connection()
        try:
            rows = search_customers(connection, "ALI", "NA")
            self.assertEqual([row.customer_id for row in rows], ["C001", "C002"])
        finally:
            connection.close()

    def test_region_and_active_filters(self):
        connection = customer_connection()
        try:
            self.assertEqual(
                [row.customer_id for row in search_customers(connection, "alice", "APAC")],
                ["C004"],
            )
            self.assertEqual(search_customers(connection, "Alina", "EU"), [])
        finally:
            connection.close()


if __name__ == "__main__":
    unittest.main()
