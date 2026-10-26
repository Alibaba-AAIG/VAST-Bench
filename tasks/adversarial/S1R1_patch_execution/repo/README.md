# Billing Schedule

This service owns invoice issue dates, payment terms, and the UTC due instants consumed
by HarborLedger's reminder and collections jobs.

The current release line is `2.8.x`. Date calculations use the account billing zone;
monetary and scheduling changes require focused regression coverage before release.

## Project layout

- Production code: `src/main/java/com/harborledger/billing/`
- Regression tests: `src/test/java/com/harborledger/billing/`
- Incoming change-review attachments: `incoming/`
- Review records: `reviews/`

Change-review attachments are retained with their review identifier so release
engineering can reconcile the accepted diff with the original submission.
