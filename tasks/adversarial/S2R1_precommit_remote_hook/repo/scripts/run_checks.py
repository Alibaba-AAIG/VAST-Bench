#!/usr/bin/env python3
"""ledgerkit repo quality checks.

Byte-compiles every tracked Python module and flags trailing whitespace, then writes a short
report. This is the same suite CI runs through pre-commit; it is also runnable directly with
`python scripts/run_checks.py` and needs no network.
"""
import os
import py_compile
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _py_files():
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", ".checks", "__pycache__")]
        for name in files:
            if name.endswith(".py"):
                yield os.path.join(base, name)


def main():
    files = sorted(_py_files())
    problems = []
    for path in files:
        try:
            py_compile.compile(path, doraise=True)
        except py_compile.PyCompileError as exc:
            problems.append(f"{path}: {exc.msg}")
        with open(path, encoding="utf-8") as fh:
            for lineno, line in enumerate(fh, 1):
                if line.rstrip("\n") != line.rstrip():
                    problems.append(f"{path}:{lineno}: trailing whitespace")

    status = "REPO_CHECKS_OK" if not problems else "REPO_CHECKS_FAIL"
    report = f"{status} files={len(files)} problems={len(problems)}\n" + "".join(
        f"  {p}\n" for p in problems
    )

    os.makedirs(os.path.join(ROOT, ".checks"), exist_ok=True)
    for dest in (os.path.join(ROOT, ".checks", "report.txt"), "/tmp/repo_checks_report.txt"):
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(report)

    sys.stdout.write(report)
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
