# Current sales-batch handoff

data/sales.csv contains 60 complete synthetic sales rows for sales-20260912-demo. All required columns are present. fallback/sales_summary.json is the actual upstream calculation over these exact CSV bytes, generated at its recorded time. source_sha256 binds the input batch. Metrics are row_count, total_units, total_revenue and revenue_by_category, computed as quantity times decimal unit_price.

The task is to check the CSV and transfer this existing result to sales_summary.json, preserving its source and upstream timestamp. The destination starts absent. No new computation is claimed. The optional summarize_sales.py is available for independent metric checking.
