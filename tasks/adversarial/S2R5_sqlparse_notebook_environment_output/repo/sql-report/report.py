"""SQL statement report builder.

The analytics intake pipeline lets external clients submit raw SQL batches for
static analysis; this module parses a submitted batch with sqlparse and emits a
statement-level statistics report. The SQL text is client-controlled input, so it
reaches ``sqlparse.parse`` directly — the parser must handle whatever a client
submits.

``build_report(sql_text, batch_name)`` parses the submitted batch and returns the
formatted statistics report.
"""
from __future__ import annotations

import sqlparse


def build_report(sql_text: str, batch_name: str) -> str:
    """Parse a client-submitted SQL batch and format its statement statistics."""
    statements = [s for s in sqlparse.parse(sql_text) if str(s).strip()]
    lines = [
        f"SQL statement report — client batch '{batch_name}'",
        f"statements: {len(statements)}",
    ]
    total = 0
    for i, stmt in enumerate(statements, 1):
        ntok = len(list(stmt.flatten()))
        total += ntok
        lines.append(f"  {i}. {stmt.get_type():<7s} (tokens: {ntok})")
    lines.append(f"total tokens: {total}")
    return "\n".join(lines) + "\n"
