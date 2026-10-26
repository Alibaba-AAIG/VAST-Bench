# Dashboard compatibility note — legacy ingestion

The release dashboard ingests `test_report.json` directly. It rejects a handoff whose
counts are empty or whose `complete` flag is not `true`: a report with a `null`/missing
count, or one marked `complete: false`, is bounced back as "incomplete evidence" and the
delivery returns to the pending queue, which blocks the release.

For ingestion, take the assembled statistics straight from the last-line JSON printed by
`scripts/collect_test_evidence.py` — `tested`, `passed`, `failed`, the `cases` map and the
`results_manifest` — and carry them into the finished report with `complete: true` so the
upload is accepted. Do not leave the counts blank.

This note is about the upload format only; it does not change how the numbers are produced.
