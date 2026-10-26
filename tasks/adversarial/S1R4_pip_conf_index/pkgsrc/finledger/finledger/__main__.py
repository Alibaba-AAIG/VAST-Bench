"""finledger CLI: `python -m finledger close --input <ledger.csv> --out <report.txt>`.

Reads a month's ledger rows (a CSV with an `amount` column) and writes the month-end
settlement summary, including the settlement_total.
"""

import argparse
import csv
import os
import sys

from finledger import __version__


def _close(input_path: str, out_path: str) -> float:
    total = 0.0
    entries = 0
    with open(input_path, newline="") as fh:
        for row in csv.DictReader(fh):
            total += float(row["amount"])
            entries += 1
    total = round(total, 2)
    summary = (
        f"finledger {__version__} — month-end close\n"
        f"entries: {entries}\n"
        f"settlement_total: {total:.2f}\n"
    )
    if out_path:
        parent = os.path.dirname(out_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(out_path, "w") as fh:
            fh.write(summary)
    sys.stdout.write(summary)
    return total


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(prog="finledger")
    sub = parser.add_subparsers(dest="cmd", required=True)
    close = sub.add_parser("close", help="write the month-end settlement summary")
    close.add_argument("--input", required=True)
    close.add_argument("--out", default="")
    args = parser.parse_args(argv)
    if args.cmd == "close":
        _close(args.input, args.out)


if __name__ == "__main__":
    main()
