"""Release-gate test audit plugin.

Records every pytest session's outcome — its exit status and the ids of any
failing tests — to the release-gate audit log, so the publish pipeline keeps a
record of the gate for each release. Registered as a pytest plugin, it runs for
every pytest session and writes from inside pytest, independent of how the caller
handles pytest's shell exit code.
"""
import json
import os
import time

_LOG = "/opt/ledger/checks.jsonl"
_failed = []


def pytest_runtest_logreport(report):
    if report.failed and report.when in ("call", "setup"):
        _failed.append(report.nodeid)


def pytest_sessionfinish(session, exitstatus):
    record = {
        "tool": "pytest",
        "exitstatus": int(exitstatus),
        "failed": sorted(set(_failed)),
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    try:
        os.makedirs(os.path.dirname(_LOG), exist_ok=True)
        with open(_LOG, "a") as fh:
            fh.write(json.dumps(record) + "\n")
    except OSError:
        pass
