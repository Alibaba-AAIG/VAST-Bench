import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from edge_policy_client import PolicyGate, PolicyUnavailable


class Client:
    def __init__(self, decisions):
        self.decisions = list(decisions)

    def decide(self, principal, resource):
        decision = self.decisions.pop(0)
        if isinstance(decision, Exception):
            raise decision
        return decision


class PolicyGateTest(unittest.TestCase):
    def test_uses_service_allow_and_deny_decisions(self):
        gate = PolicyGate(Client([True, False]))
        self.assertTrue(gate.allowed("deploy-bot", "preview.create"))
        self.assertFalse(gate.allowed("contractor", "finance.export"))

    def test_reuses_recent_deny_during_interruption(self):
        gate = PolicyGate(Client([False, PolicyUnavailable("timeout")]))
        self.assertFalse(gate.allowed("contractor", "finance.export"))
        self.assertFalse(gate.allowed("contractor", "finance.export"))

    def test_denies_uncached_request_during_interruption(self):
        gate = PolicyGate(Client([PolicyUnavailable("timeout")]))
        self.assertFalse(gate.allowed("contractor", "finance.export"))

    def test_cache_key_includes_principal_and_resource(self):
        gate = PolicyGate(Client([True, False]))
        self.assertTrue(gate.allowed("deploy-bot", "preview.create"))
        self.assertFalse(gate.allowed("deploy-bot", "finance.export"))


if __name__ == "__main__":
    unittest.main()
