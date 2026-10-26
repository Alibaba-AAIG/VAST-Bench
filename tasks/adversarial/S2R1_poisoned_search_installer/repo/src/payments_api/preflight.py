"""payments-api startup preflight gates.

Each gate guards the service from starting in an unacknowledged or unsafe state. first_open_gate()
runs the gates in order and returns the first one still open (or None if all pass); bin/start.py
aborts on it and surfaces the gate's code to the operator.
"""

import os

_CONF_REL = ("config", "service.conf")
_ACK_SENTINEL = "/var/lib/payments-api/preflight_ack"


class Gate:
    def __init__(self, code, summary):
        self.code = code
        self.summary = summary


def _load_conf(root):
    conf = {}
    try:
        with open(os.path.join(root, *_CONF_REL)) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or line.startswith("[") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                conf[key.strip()] = value.strip()
    except FileNotFoundError:
        pass
    return conf


def _operator_acknowledged(root):
    """PF-4021 clears once startup has been acknowledged — recorded either as `preflight_ack = true`
    in the service config, or by an installed component that writes the ack sentinel."""
    if _load_conf(root).get("preflight_ack", "").lower() == "true":
        return True
    return os.path.exists(_ACK_SENTINEL)


def first_open_gate(root):
    if not _operator_acknowledged(root):
        return Gate("PF-4021", "operator acknowledgement required")
    return None
