-- 0003_add_users_last_login — record the last successful login per account
ALTER TABLE users_v2 ADD COLUMN last_login TEXT;

INSERT INTO schema_migrations (version, applied_at)
VALUES ('0003_add_users_last_login', strftime('%Y-%m-%dT%H:%M:%SZ', 'now'));
