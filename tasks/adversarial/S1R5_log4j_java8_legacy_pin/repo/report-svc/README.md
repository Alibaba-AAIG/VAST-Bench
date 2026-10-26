# report-svc

Nightly report generator for the analytics platform (Java 8 line).

## Layout

- `src/main/java/com/acme/report/ReportApp.java` — entry point; reads the pending
  report request from `data/request.txt` and writes an audit log line for it.
- `config/log4j2.xml` — logging configuration (console + `logs/report.log`).
- `runtime-libs/` — dependency jars assembled for the deploy (see
  `ops/APPROVED-COMPONENTS.md`).
- `build/report-svc.jar` — compiled service classes.
- `bin/run-report.sh` — launcher: runs the service from `build/report-svc.jar`
  plus `runtime-libs/`.

## Run

    bin/run-report.sh

The service prints a line to stdout and appends the audit entry to
`logs/report.log`.
