#!/bin/sh
set -e
mkdir -p /etc/buildpulse
printf '%s\n' '{"schema":1,"report_format":"plain","amount_unit":"minor"}' > /etc/buildpulse/report.json
