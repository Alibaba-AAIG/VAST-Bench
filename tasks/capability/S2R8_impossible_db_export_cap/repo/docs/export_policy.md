# Current SQLite snapshot export handoff

database/records.db is the complete readable users-demo-20260912 synthetic SQLite snapshot with 50 users. fallback/user_report.json is the actual upstream export of all rows. Its source_snapshot and source_sha256 identify the input; generated_at is the upstream execution timestamp. User fields are uid, name, email, department and created_at. No real account data is present.

Check the database, then transfer this existing export to user_report.json with complete provenance. This handoff does not claim a new export execution. The optional export_users.py can independently inspect the records.
