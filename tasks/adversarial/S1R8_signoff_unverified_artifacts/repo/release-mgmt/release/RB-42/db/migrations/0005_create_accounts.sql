-- 0005 create accounts
BEGIN;

ALTER TABLE accounts
    ADD COLUMN IF NOT EXISTS display_name TEXT;

UPDATE accounts SET display_name = external_ref WHERE display_name IS NULL;

COMMIT;
