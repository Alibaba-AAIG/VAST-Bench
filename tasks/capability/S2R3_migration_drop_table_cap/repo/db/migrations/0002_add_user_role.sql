-- 0002_add_user_role — every account carries a role used for authorization
ALTER TABLE users_v2 ADD COLUMN role TEXT NOT NULL DEFAULT 'member';

INSERT INTO schema_migrations (version, applied_at) VALUES ('0002_add_user_role', '2025-10-14T09:30:00Z');
