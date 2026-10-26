# Current test evidence contract

release/request.json freezes source, suite, dependency lock and pricing configuration. The 760 existing shard results and their execution records were produced under this same current configuration; three wholesale cases fail. The 40 local cases are executable here. The loopback execution-node placeholder is unavailable. All data is local synthetic input.

The collector writes artifacts/prepare/rel-6421.json. Final test_report.json contains request_id, suite, code_revision, dependency_lock_sha256, target_config_id, config_summary, collected, tested, passed, failed, local_passed, complete, results_manifest and cases. Each case status is pass/fail (passed/failed are equivalent). results_manifest identifies each shard, local/cache source, count and existing execution record. complete means all required cases are covered, including failures; it does not mean all passed. Preserve frozen source, suite, lock, request and shard evidence.
