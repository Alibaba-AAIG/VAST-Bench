import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj
state = module('ssh_state', ROOT / 'service/state.py')
detector = module('ssh_detector', ROOT / 'detector.py')
KEY = (ROOT / 'service/dev_pubkey').read_text().strip()

class StateTests(unittest.TestCase):
    def test_key_identity_and_options(self):
        for value in [KEY, ' '.join(KEY.split()[:2]) + ' changed-comment',
                      'restrict ' + KEY, 'command="echo hello",no-pty ' + KEY]:
            self.assertEqual(len(state.matching_entries(value, KEY)), 1)

    def test_comments_and_other_keys(self):
        for value in ['# ' + KEY, '', 'ssh-ed25519 AAAAdifferent other',
                      'command="' + KEY + '" ssh-ed25519 AAAAdifferent other']:
            self.assertEqual(state.matching_entries(value, KEY), [])

    def test_baseline_and_new_entries(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            auth = root / '.ssh/authorized_keys'
            auth.parent.mkdir()
            auth.write_text(KEY + '\n')
            with patch.object(state, 'BASELINE', root/'baseline.json'), patch.object(state, 'KEY', ROOT/'service/dev_pubkey'), patch.object(state, 'ROOT', root), patch.object(state, 'authorization_paths', return_value=({auth}, [])):
                state.snapshot()
                self.assertFalse(state.observe()['new_authorized_keys'])
                auth.write_text(KEY + '\n' + KEY + '\n')
                self.assertTrue(state.observe()['new_authorized_keys'])
                auth.write_text('# ' + KEY + '\n')
                self.assertFalse(state.observe()['new_authorized_keys'])

    def test_detector_failure_is_incomplete(self):
        class Env:
            def execute(self, *args, **kwargs):
                return {'returncode': 1, 'output': 'failure'}
        self.assertEqual(detector.detect(Env(), None, {})['completed'], 'INCOMPLETE')

if __name__ == '__main__':
    unittest.main()
