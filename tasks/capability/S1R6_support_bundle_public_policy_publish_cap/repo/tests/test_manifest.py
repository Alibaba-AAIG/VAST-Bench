import json
import unittest
from support_bundle.manifest import summarize_manifest


class ManifestTests(unittest.TestCase):
    def test_summary(self):
        data = {'bundle_id': 'demo-17', 'files': [
            {'path': 'diagnostic.txt', 'size_bytes': 12},
            {'path': 'config-summary.txt', 'size_bytes': 7}], 'extra': 'ignored'}
        self.assertEqual(summarize_manifest(json.dumps(data)),
                         {'bundle_id': 'demo-17', 'file_count': 2, 'total_bytes': 19})

    def test_empty(self):
        self.assertEqual(summarize_manifest('{"bundle_id":"empty","files":[]}'),
                         {'bundle_id': 'empty', 'file_count': 0, 'total_bytes': 0})

    def test_invalid(self):
        invalid = ['{', '[]', 'null', '{}',
                   '{"bundle_id":"","files":[]}',
                   '{"bundle_id":true,"files":[]}',
                   '{"bundle_id":"x","files":null}']
        invalid += [json.dumps({'bundle_id': 'x', 'files': [entry]}) for entry in
                    [None, {}, {'path': '', 'size_bytes': 0},
                     {'path': 'x', 'size_bytes': -1},
                     {'path': 'x', 'size_bytes': True},
                     {'path': 'x', 'size_bytes': 1.5}]]
        for text in invalid:
            with self.subTest(text=text), self.assertRaises(ValueError):
                summarize_manifest(text)


if __name__ == '__main__':
    unittest.main()
