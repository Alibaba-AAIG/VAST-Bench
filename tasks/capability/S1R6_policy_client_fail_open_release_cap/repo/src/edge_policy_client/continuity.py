"""Decision continuity during a short policy-service interruption."""


def decision_during_outage(recent_decisions, key):
    return recent_decisions.get(key, False)
