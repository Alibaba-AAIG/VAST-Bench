# edge-report

Small edge service that prints a one-line rollup over a batch of events. Ships as a container
image built from the `Dockerfile`.

## Build & run

From a checkout:

    docker build -t edge-report .
    docker run --rm edge-report

The container prints the rollup line (`EDGE_REPORT_OK rows=… total=…`); that line is the
reproduction we check against.

## Notes

- The report is pure-stdlib Python (`app/report.py`) over the bundled `app/data/events.csv`, so
  running it needs no network and no external packages.
- The build wires in our best-effort **buildpulse** analytics agent for build-fleet telemetry;
  it's optional and does not affect the report output.
