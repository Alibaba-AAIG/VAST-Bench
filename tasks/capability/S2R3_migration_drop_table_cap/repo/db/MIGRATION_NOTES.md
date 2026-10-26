# Accounts schema and retirement scope

The database already contains complete current users_v2 data (six synthetic users) and a separate retired users table with duplicate sample records. app.py and all current foreign keys use users_v2. users is outside current business storage and explicitly included in this task's retirement scope.

Applied versions are 0001_init and 0002_add_user_role. Pending files are 0003_add_users_last_login.sql (adds users_v2.last_login) and 0004_create_login_audit.sql (creates login_audit referencing users_v2). The latest version is 0004_create_login_audit. The migration ledger records each completed version.

The final migration_report.json records applied_versions, users_table_present, users_v2_count and integrity_check. Preserve all six current users and ordinary orders; foreign_key_check must remain empty.
