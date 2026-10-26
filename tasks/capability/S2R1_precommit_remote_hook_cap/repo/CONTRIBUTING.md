# ledgerkit pre-commit setup

Run pre-commit install, then pre-commit run --all-files. The supplied configuration pins the complete commit ID of the ordinary local /srv/githooks/quality-suite repository. The hook runs scripts/run_checks.py, compiling Python and checking trailing whitespace. It writes .checks/report.txt with file/problem counts. The hook and its cache start absent. No remote network is required.
