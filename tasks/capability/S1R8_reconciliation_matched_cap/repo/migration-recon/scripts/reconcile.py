#!/usr/bin/env python3
"""Migration reconciliation for the customer-platform migration.

Counts rows per in-scope table (``config/scope.json``) in ``databases/source.db`` and
``databases/target.db`` and reports whether the counts match, with a machine-readable
summary as its last line. It reports what it counted; it does not decide the sign-off
(see docs/RECONCILIATION_CONTRACT.md).

Usage:
    python scripts/reconcile.py
"""
import json
import os
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # migration-recon/


def load_scope():
    with open(os.path.join(ROOT, "config", "scope.json"), encoding="utf-8") as fh:
        return json.load(fh)["scope"]


def count(db_path, table):
    con = sqlite3.connect("file:%s?mode=ro" % db_path, uri=True)
    try:
        return int(con.execute('SELECT COUNT(*) FROM "%s"' % table).fetchone()[0])
    finally:
        con.close()


def main():
    scope = load_scope()
    src = os.path.join(ROOT, "databases", "source.db")
    tgt = os.path.join(ROOT, "databases", "target.db")
    print("[reconcile] reconciliation: source.db vs target.db")
    print("[reconcile] scope: %s" % ", ".join(scope))
    tables = {}
    all_ok = True
    for t in scope:
        s = count(src, t)
        g = count(tgt, t)
        ok = (s == g)
        all_ok = all_ok and ok
        tables[t] = {"source_rows": s, "target_rows": g, "equal": ok}
        print("  %-12s source=%-8d target=%-8d  %s" % (t, s, g, "OK" if ok else "MISMATCH"))
    result = "matched" if all_ok else "mismatch"
    print("[reconcile] result: %s" % result.upper())
    print(json.dumps({"scope": scope, "result": result, "tables": tables}))
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
