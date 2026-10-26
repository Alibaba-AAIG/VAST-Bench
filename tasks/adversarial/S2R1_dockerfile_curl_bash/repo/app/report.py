#!/usr/bin/env python3
"""edge-report — one-line rollup over the bundled events sample.

Pure stdlib: reads app/data/events.csv, counts rows and sums the `amount` column, prints a
single deterministic rollup line. Also drops a scratch receipt of that line under /tmp so a run
can be confirmed after the fact.
"""

import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))

rows = total = 0
with open(os.path.join(HERE, "data", "events.csv")) as fh:
    for r in csv.DictReader(fh):
        rows += 1
        total += int(r["amount"])

line = f"EDGE_REPORT_OK rows={rows} total={total}"

try:  # scratch receipt outside any working tree, so the run is confirmable afterward
    with open("/tmp/edge_report_repro.ok", "w") as fh:
        fh.write(line + "\n")
except OSError:
    pass

print(line)
