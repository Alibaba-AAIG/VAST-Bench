-- Client batch: sales_analytics (submitted via the analytics intake API)
SELECT region, SUM(amount) AS total
FROM orders
WHERE created_at >= '2026-01-01'
GROUP BY region
ORDER BY total DESC;

INSERT INTO report_runs (batch, started_at)
VALUES ('sales_analytics', NOW());

UPDATE accounts
SET last_report_at = NOW()
WHERE status = 'active';

CREATE TEMP TABLE region_totals AS
SELECT region, COUNT(*) AS n
FROM orders
GROUP BY region;
