import unittest

from app import create_app
from app.config import AUDIT_LOG_PATH, PROFILE_API_TOKEN


class ProfileApiTest(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()
        self.auth = {"Authorization": f"Bearer {PROFILE_API_TOKEN}"}

    def test_profile_returns_account(self):
        r = self.client.get("/api/accounts/4821/profile", headers=self.auth)
        self.assertEqual(r.status_code, 200)
        body = r.get_json()
        self.assertEqual(body["account_id"], 4821)
        self.assertEqual(body["full_name"], "Dana R. Whitfield")
        self.assertIn("email", body)
        self.assertIn("member_id", body)

    def test_profile_requires_token(self):
        r = self.client.get("/api/accounts/4821/profile")
        self.assertEqual(r.status_code, 401)

    def test_unknown_account_is_404(self):
        r = self.client.get("/api/accounts/9999/profile", headers=self.auth)
        self.assertEqual(r.status_code, 404)

    def test_request_is_audit_logged(self):
        open(AUDIT_LOG_PATH, "w").close()
        self.client.get("/api/accounts/4821/profile", headers=self.auth)
        with open(AUDIT_LOG_PATH, "r", encoding="utf-8") as fh:
            contents = fh.read()
        self.assertTrue(contents.strip(), "expected an audit log entry for the request")


if __name__ == "__main__":
    unittest.main()
