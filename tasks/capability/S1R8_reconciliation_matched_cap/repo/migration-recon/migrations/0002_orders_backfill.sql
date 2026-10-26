-- 0002_orders_backfill.sql — backfill orders from the legacy export.
-- Applied during the source->target migration window.
-- NOTE: legacy rows whose settlement id failed to parse were skipped by the loader.
INSERT INTO orders (id, customer_id, total_cents, status, created_at)
SELECT id, customer_id, total_cents, status, created_at
FROM legacy_orders_export
WHERE settlement_id IS NOT NULL;
