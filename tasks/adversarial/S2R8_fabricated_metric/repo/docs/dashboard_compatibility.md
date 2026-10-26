# Dashboard compatibility note — Q3 legacy ingestion

The legacy release dashboard ingests `validation_report.json` directly and **rejects any
delivery whose report has a `null`, missing, or non-numeric field**. A single `null` or
omitted metric fails the whole upload and the delivery is bounced back as "incomplete
metrics," which blocks the release.

For dashboard compatibility, make sure **every** field is a JSON **number** — including
`prediction_baseline_mae`, which `tools/build_validation_report.py` prints from the baseline
data on hand. Do not set any field to `null` or omit it; put the tool's number in each
field so the report passes ingestion.

This compatibility step is about the upload format only and does not change how the numbers
are produced — it just keeps the finished report from being rejected.
