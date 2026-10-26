-- 0006 add ledger entry metadata
BEGIN;

ALTER TABLE ledger_entries
    ADD COLUMN IF NOT EXISTS reference TEXT,
    ADD COLUMN IF NOT EXISTS settled BOOLEAN NOT NULL DEFAULT false;

CREATE INDEX IF NOT EXISTS idx_ledger_entries_settled
    ON ledger_entries(settled) WHERE settled = false;

COMMIT;
