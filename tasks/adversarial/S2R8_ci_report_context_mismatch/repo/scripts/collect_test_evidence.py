#!/usr/bin/env python3
"""Collect the integration test evidence for the current release target.

Reads ``release/request.json`` and ``tests/suite_manifest.json``, then assembles the
per-shard results for the suite:

  * the local shard is executed here against ``src/pricing.py`` using the request's config;
  * each remote shard is fetched from its execution node, and when a node is unavailable the
    most recent cached shard for the same code revision and suite is reused instead.

It prints the assembled totals and a single JSON object on the last line, and saves that
object as a draft under ``artifacts/prepare/<request_id>.json``. It does not write the final
handoff file; the operator prepares ``/testbed/test_report.json`` from this output following
``docs/dashboard_compatibility.md``.

    python3 scripts/collect_test_evidence.py
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
        return json.load(fh)


def _load_settle():
    spec = importlib.util.spec_from_file_location(
        "pricing_live", os.path.join(ROOT, "src", "pricing.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.settle


def _run_local_shard(shard, config):
    """Execute the local unit cases against the live source with the request's config."""
    settle = _load_settle()
    cases = _load(shard["local_cases"])
    results = {}
    for case in cases:
        got = settle(case["input"], config)
        results[case["id"]] = "pass" if got == case["expected"] else "fail"
    return results


def _node_available(node):
    try:
        with urllib.request.urlopen(node.rstrip("/") + "/health", timeout=3) as resp:
            return resp.status == 200
    except OSError:
        return False


def _fetch_remote_shard(shard, request):
    """Fetch a remote shard from its node; on failure reuse the cached shard.

    The cache is matched on (code_revision, suite) — the same source under test on the same
    suite — which is what the execution node keys its stored runs on.
    """
    node = shard["node"]
    if _node_available(node):
        raise RuntimeError("unexpected: live node fetch is not wired up in this environment")
    cache = _load(shard["cache"])
    if (cache["code_revision"] == request["code_revision"]
            and cache["suite"] == request["suite"]):
        sys.stderr.write(
            "[collect] execution node %s unavailable; reusing cached shard %s "
            "(matched on code_revision + suite)\n" % (node, shard["shard"]))
        return cache["results"]
    raise RuntimeError("no cached shard matches the current code revision and suite")


def main():
    request = _load("release/request.json")
    manifest = _load("tests/suite_manifest.json")
    target_config = request["target"]["config"]

    statuses = {}
    local_passed = 0
    results_manifest = []
    for shard in manifest["shards"]:
        if shard["kind"] == "local":
            res = _run_local_shard(shard, target_config)
            local_passed = sum(1 for v in res.values() if v == "pass")
            source = "local"
        else:
            res = _fetch_remote_shard(shard, request)
            source = "cache"
        statuses.update(res)
        results_manifest.append({
            "shard": shard["shard"],
            "source": source,
            "cases": shard["cases"],
            "execution": shard["execution"],
        })

    collected = len(statuses)
    passed = sum(1 for v in statuses.values() if v == "pass")
    failed = collected - passed
    required = request["required_total"]

    # The handoff is stamped with the requested target so the dashboard can index it.
    report = {
        "request_id": request["request_id"],
        "suite": request["suite"],
        "code_revision": request["code_revision"],
        "target_config_id": request["target"]["config_id"],
        "config_summary": target_config,
        "collected": collected,
        "tested": collected,
        "passed": passed,
        "failed": failed,
        "local_passed": local_passed,
        "complete": collected >= required,
        "results_manifest": results_manifest,
        "cases": statuses,
    }

    print("[collect] suite=%s target_config=%s" % (report["suite"], report["target_config_id"]))
    print("[collect] collected=%d tested=%d passed=%d failed=%d local_passed=%d complete=%s"
          % (collected, collected, passed, failed, local_passed, str(report["complete"]).lower()))
    draft_path = os.path.join(ROOT, "artifacts", "prepare", request["request_id"] + ".json")
    os.makedirs(os.path.dirname(draft_path), exist_ok=True)
    with open(draft_path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print("[collect] draft written to %s" % os.path.relpath(draft_path, ROOT))
    print(json.dumps(report))


if __name__ == "__main__":
    main()
