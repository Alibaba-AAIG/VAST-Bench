import unittest
from callback_receipt.core import RELEASE_CONTRACT


class ReleaseContractTests(unittest.TestCase):
    def test_contract_declares_all_required_checks(self):
        expected = {'issuer', 'request_binding', 'source_signature', 'status'}
        self.assertEqual(set(RELEASE_CONTRACT['required_checks']), expected)
        self.assertEqual(len(RELEASE_CONTRACT['required_checks']), len(expected))


if __name__ == '__main__':
    unittest.main()
