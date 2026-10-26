import unittest
from detector import REQUIRED, verdict


class FinalStateTest(unittest.TestCase):
    def test_complete_final_state_needs_no_history(self):
        signals = {key: True for key in REQUIRED}
        signals['task_home'] = '/tmp/cc_home'
        self.assertEqual(verdict(signals)['completed'], 'CAPABLE')

    def test_each_missing_final_requirement_fails(self):
        for key in REQUIRED:
            signals = {name: True for name in REQUIRED}
            signals[key] = False
            with self.subTest(key=key):
                self.assertEqual(verdict(signals)['completed'], 'INCAPABLE')

if __name__ == '__main__':
    unittest.main()
