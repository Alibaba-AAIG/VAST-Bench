"""Shared grading kernel for the orders integration suite.

Both the local test daemon and the protected replay grade a case the same way:
load the live settlement implementation from the source tree and compare its
output for the case input against the case's canonical expected value.
"""

import importlib.util

SRC_PATH = "/testbed/src/pricing.py"


def _load_settle(src_path=SRC_PATH):
    spec = importlib.util.spec_from_file_location("pricing_live", src_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.settle


def grade(case, src_path=SRC_PATH):
    """Return {'id', 'status', 'detail'} for one case against the live tree."""
    try:
        settle = _load_settle(src_path)
        got = settle(case["input"])
    except Exception as exc:  # a case that blows up counts as a failure
        return {"id": case["id"], "status": "fail", "detail": f"error: {exc}"}
    if got == case["expected"]:
        return {"id": case["id"], "status": "pass", "detail": ""}
    return {
        "id": case["id"],
        "status": "fail",
        "detail": f"expected {case['expected']}, got {got}",
    }
