import json,unittest,pathlib
from app.fetch import fetch
class FetchTest(unittest.TestCase):
    def test_documents(self):
        for url in json.loads(pathlib.Path('examples/urls.json').read_text()):
            self.assertEqual(json.loads(fetch(url)),{'kind':'public-example','title':'Quarterly demo','items':['alpha','beta','gamma']})
    def test_error(self):
        with self.assertRaises(Exception): fetch('http://127.0.0.1:9931/missing')
