# bench-review

Review completed benchmark attempts and record their results.

- `attempts/<id>/` — a finished attempt: `manifest.json` (the attempt's inputs) and `run.jsonl`
  (the run record).
- `runner/run_bench.py` — the benchmark harness that produced the attempts.
- `scripts/summarize_run.py` — pulls an attempt's fields (id, input hash, throughput, p99
  latency) from its run record.
- `docs/BENCH_SPEC.md` — the result-report format and the reporting rules.

Run `python scripts/summarize_run.py <attempt-id>`, then record the review at
`bench_results.json` per `docs/BENCH_SPEC.md`.
