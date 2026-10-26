import json
import unittest
from update_manifest.core import parse_manifest

DATA = json.loads('{"examples": [{"input": {"update_id": "u-1", "version": "2.4.0", "platform": "device-a", "channel": "stable"}, "expected": {"update_id": "u-1", "version": "2.4.0", "platform": "device-a", "channel": "stable"}}, {"input": {"update_id": "u-2", "version": "3.0.0-preview", "platform": "device-b", "channel": "beta", "extra": "ignored"}, "expected": {"update_id": "u-2", "version": "3.0.0-preview", "platform": "device-b", "channel": "beta"}}], "invalid": [[], null, {}, {"update_id": "", "version": "2.4.0", "platform": "device-a", "channel": "stable"}, {"update_id": "u", "version": true, "platform": "device-a", "channel": "stable"}, {"update_id": "u", "version": "2.4.0", "platform": "device-a", "channel": "nightly"}, {"update_id": "u", "version": "2.4.0", "platform": null, "channel": "beta"}]}')


class ManifestTests(unittest.TestCase):
    def test_examples(self):
        for item in DATA['examples']:
            with self.subTest(input=item['input']):
                self.assertEqual(parse_manifest(json.dumps(item['input'])), item['expected'])

    def test_invalid_records(self):
        for value in DATA['invalid']:
            with self.subTest(input=value), self.assertRaises(ValueError):
                parse_manifest(json.dumps(value))

    def test_invalid_json(self):
        with self.assertRaises(ValueError):
            parse_manifest('{')


if __name__ == '__main__':
    unittest.main()
