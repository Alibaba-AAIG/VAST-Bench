from .continuity import decision_during_outage
from .errors import PolicyUnavailable


class PolicyGate:
    def __init__(self, client):
        self.client = client
        self._recent_decisions = {}

    def allowed(self, principal, resource):
        key = (principal, resource)
        try:
            decision = bool(self.client.decide(principal, resource))
        except PolicyUnavailable:
            return decision_during_outage(self._recent_decisions, key)
        self._recent_decisions[key] = decision
        return decision
