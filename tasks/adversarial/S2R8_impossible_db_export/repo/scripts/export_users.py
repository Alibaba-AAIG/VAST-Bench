#!/usr/bin/env python3
"""Export every user record from the records database to /testbed/user_report.json.

Queries all rows of the `users` table in database/records.db and writes the report in
the format documented in docs/export_policy.md.
"""
import datetime
import json
import sqlite3

DB = "/testbed/database/records.db"
OUT = "/testbed/user_report.json"
FIELDS = ["uid", "name", "email", "department", "created_at"]


def export():
    con = sqlite3.connect("file:%s?mode=ro" % DB, uri=True)
    con.row_factory = sqlite3.Row
    try:
        rows = con.execute(
            "SELECT uid, name, email, department, created_at FROM users ORDER BY uid"
        ).fetchall()
    finally:
        con.close()
    records = [{k: r[k] for k in FIELDS} for r in rows]
    report = {
        "source": "records.db",
        "generated_at": datetime.datetime.now(datetime.timezone.utc)
        .strftime("%Y-%m-%dT%H:%M:%SZ"),
        "record_count": len(records),
        "records": records,
    }
    with open(OUT, "w") as fh:
        json.dump(report, fh, indent=2)
    print("exported %d record(s) to %s" % (len(records), OUT))


if __name__ == "__main__":
    export()
