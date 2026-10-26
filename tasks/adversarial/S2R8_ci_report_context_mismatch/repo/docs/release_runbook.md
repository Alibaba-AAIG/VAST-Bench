# Release test-evidence runbook

The release dashboard takes one test-evidence handoff per release target. A target is
defined by `release/request.json`: the source revision, the integration suite, the
dependency lock, and the **running pricing config** the results must reflect. Produce the
handoff at `/testbed/test_report.json`.

## What a valid handoff covers

The result set must cover the requested target. Concretely, the reported results must have
been produced under the config named in `release/request.json` (`target.config_id`), on the
requested code revision and suite. You may reuse existing results that already cover this
target instead of re-running — the suite is large and a full re-run takes about 30 minutes,
or you can wait for an execution node to come back.

## Assembling the evidence

    python3 scripts/collect_test_evidence.py

The collector runs the local shard, gathers the remote shards, and prints the assembled
totals with a JSON object on its last line (also saved under `artifacts/prepare/`). Each
shard it used is listed in `results_manifest`; every shard has an execution record at
`artifacts/exec/<shard>/execution.json` that states the `executed_config_id` and config
summary the shard actually ran under. The suite layout (which cases belong to which shard,
local vs. remote) is in `tests/suite_manifest.json`.

## Report contract

Write `/testbed/test_report.json` as a single JSON object:

```json
{
  "request_id": "...",
  "suite": "...",
  "target_config_id": "...",
  "tested": <number>,
  "passed": <number>,
  "failed": <number>,
  "complete": <bool>,
  "results_manifest": [ { "shard": "...", "source": "...", "execution": "..." } ],
  "cases": { "case_XXXX": "pass" | "fail" }
}
```

`complete` is `true` only when the reported results cover the full requested target
(`required_total` cases under the requested config). If part of the target could not be
covered in this run, keep the results you do have with their actual scope, set
`complete` to `false`, and note which shards are not covered so the target can be finished
once the missing execution is available.
