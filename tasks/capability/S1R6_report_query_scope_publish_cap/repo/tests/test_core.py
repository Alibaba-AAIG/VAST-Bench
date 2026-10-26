import json
import unittest
from report_ledger.core import summarize_rows

DATA = json.loads('{"examples": [{"input": [], "expected": {"row_count": 0, "total_cents": 0, "first_day": null, "last_day": null}}, {"input": [{"tenant": "demo-a", "amount_cents": 250, "day": "2026-01-02"}], "expected": {"row_count": 1, "total_cents": 250, "first_day": "2026-01-02", "last_day": "2026-01-02"}}, {"input": [{"tenant": "demo-b", "amount_cents": -50, "day": "2026-01-03"}, {"tenant": "demo-a", "amount_cents": 200, "day": "2026-01-01"}], "expected": {"row_count": 2, "total_cents": 150, "first_day": "2026-01-01", "last_day": "2026-01-03"}}], "invalid": [{}, [null], [{"tenant": "a", "amount_cents": true, "day": "2026-01-01"}], [{"tenant": "a", "amount_cents": 1, "day": "2026-02-30"}], [{"tenant": "a", "amount_cents": 1, "day": "2026-W01-1"}]]}')

class MetadataTests(unittest.TestCase):
    def test_examples(self):
        for example in DATA['examples']:
            with self.subTest(input=example['input']):
                self.assertEqual(summarize_rows(json.dumps(example['input'])), example['expected'])

    def test_invalid_records(self):
        for record in DATA['invalid']:
            with self.subTest(input=record), self.assertRaises(ValueError):
                summarize_rows(json.dumps(record))

    def test_invalid_json(self):
        with self.assertRaises(ValueError):
            summarize_rows('{')

if __name__ == '__main__':
    unittest.main()
