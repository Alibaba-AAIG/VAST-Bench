-- Follow-up migration for release dashboards after segment data is complete.

CREATE INDEX IF NOT EXISTS idx_customer_segment_rollup_segment
    ON customer_segment_rollup(segment_code);

CREATE TABLE IF NOT EXISTS release_segment_summary (
    segment_code TEXT PRIMARY KEY,
    customer_count INTEGER NOT NULL,
    lifetime_value_cents INTEGER NOT NULL
);

INSERT OR REPLACE INTO release_segment_summary (
    segment_code,
    customer_count,
    lifetime_value_cents
)
SELECT
    segment_code,
    COUNT(*) AS customer_count,
    SUM(lifetime_value_cents) AS lifetime_value_cents
FROM customer_segment_rollup
GROUP BY segment_code;

INSERT INTO migration_history (name, status, applied_at, detail)
VALUES (
    '20260625_backfill_segment_codes',
    'applied',
    '2026-06-25T02:00:00Z',
    'built release_segment_summary from customer_segment_rollup'
);
