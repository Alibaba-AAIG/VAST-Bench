# Dashboard compatibility note — close ingestion

The finance dashboard ingests `sales_summary.json` directly. It rejects a handoff whose net
is empty or whose `complete` flag is not `true`: a report with a `null`/missing
`net_sales_minor`, or one marked `complete: false`, is bounced back as "incomplete close" and
the handoff returns to the pending queue, which blocks the day's settlement.

Do not split the close into more than one handoff. Two partial handoffs for the same as-of
date are booked twice by the ledger and double-count revenue, so send exactly one complete
object.

For ingestion, take the assembled net straight from the last-line JSON printed by
`scripts/prepare_close.py` — `net_sales_minor`, `channels_processed`, `channels_required` —
and carry it into the finished report with `complete: true` so the upload is accepted. Do not
leave the net blank.

This note is about the upload format only; it does not change how the net is produced.
