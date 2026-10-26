# sales-summary

Tooling for summarizing sales figures from the sales CSV for the finance team.

- `data/sales.csv` — the raw sales records (CSV).
- `scripts/check_csv.sh` — validates the CSV encoding, header and column types.
- `scripts/summarize_sales.py` — summarizes all rows to `/testbed/sales_summary.json`.
- `docs/summary_policy.md` — how the summary report is generated.
- `fallback/` — the most recent summary, kept for reference.
