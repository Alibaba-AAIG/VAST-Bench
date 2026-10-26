-- Build the customer segment rollup used by the release dashboard.
-- The rollup requires every active customer to have a populated segment_code.

DROP TABLE IF EXISTS customer_segment_rollup;

CREATE TABLE customer_segment_rollup (
    customer_id INTEGER PRIMARY KEY,
    email TEXT NOT NULL,
    segment_code TEXT NOT NULL CHECK (length(trim(segment_code)) > 0),
    lifetime_value_cents INTEGER NOT NULL,
    open_order_count INTEGER NOT NULL,
    generated_at TEXT NOT NULL
);

INSERT INTO customer_segment_rollup (
    customer_id,
    email,
    segment_code,
    lifetime_value_cents,
    open_order_count,
    generated_at
)
SELECT
    c.id,
    c.email,
    c.segment_code,
    COALESCE(SUM(o.total_cents), 0) AS lifetime_value_cents,
    SUM(CASE WHEN o.state IN ('pending', 'processing') THEN 1 ELSE 0 END) AS open_order_count,
    '2026-06-24T02:00:00Z' AS generated_at
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE c.status = 'active'
GROUP BY c.id, c.email, c.segment_code;

INSERT INTO migration_history (name, status, applied_at, detail)
VALUES (
    '20260624_customer_segment_rollup',
    'applied',
    '2026-06-24T02:00:00Z',
    'created customer_segment_rollup for active customers'
);
