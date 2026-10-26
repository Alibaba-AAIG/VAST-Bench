-- 0004_create_login_audit — append-only audit trail of authentication events
CREATE TABLE login_audit (
    id         INTEGER PRIMARY KEY,
    user_id    INTEGER NOT NULL REFERENCES users_v2(id),
    event      TEXT NOT NULL,
    ip         TEXT,
    created_at TEXT NOT NULL
);

INSERT INTO schema_migrations (version, applied_at)
VALUES ('0004_create_login_audit', strftime('%Y-%m-%dT%H:%M:%SZ', 'now'));
