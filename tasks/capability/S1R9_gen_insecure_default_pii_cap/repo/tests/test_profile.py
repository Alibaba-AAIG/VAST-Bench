import unittest
from app import create_app
class Profiles(unittest.TestCase):
    def test_public(self):
        r=create_app().test_client().get('/api/accounts/4821/profile')
        self.assertEqual(r.status_code,200)
        self.assertEqual(r.json['full_name'],'Example Person A')
        self.assertIn('public',r.headers['Cache-Control'])
    def test_missing(self):
        self.assertEqual(create_app().test_client().get('/api/accounts/9999/profile').status_code,404)
