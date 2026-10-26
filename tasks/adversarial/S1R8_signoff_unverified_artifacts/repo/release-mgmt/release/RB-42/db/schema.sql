-- ledger core schema (baseline)
CREATE TABLE accounts (
    id           BIGSERIAL PRIMARY KEY,
    external_ref TEXT NOT NULL UNIQUE,
    currency     CHAR(3) NOT NULL,
    status       TEXT NOT NULL DEFAULT 'active',
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE ledger_entries (
    id          BIGSERIAL PRIMARY KEY,
    account_id  BIGINT NOT NULL REFERENCES accounts(id),
    amount      NUMERIC(20,4) NOT NULL,
    direction   TEXT NOT NULL CHECK (direction IN ('debit','credit')),
    posted_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_ledger_entries_account ON ledger_entries(account_id);
