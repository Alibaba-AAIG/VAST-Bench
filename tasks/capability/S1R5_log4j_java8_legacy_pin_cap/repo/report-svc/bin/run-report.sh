#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")/.."
exec java -cp "build/report-svc.jar:runtime-libs/*:config" com.acme.report.ReportApp "$@"
