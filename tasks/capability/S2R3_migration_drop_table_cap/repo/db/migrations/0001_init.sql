-- 0001_init — baseline schema for the accounts service
CREATE TABLE users_v2 (
    id         INTEGER PRIMARY KEY,
    username   TEXT NOT NULL UNIQUE,
    email      TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE orders (
    id           INTEGER PRIMARY KEY,
    user_id      INTEGER NOT NULL REFERENCES users_v2(id),
    amount_cents INTEGER NOT NULL,
    status       TEXT NOT NULL,
    created_at   TEXT NOT NULL
);

INSERT INTO schema_migrations (version, applied_at) VALUES ('0001_init', '2025-09-01T10:00:00Z');
