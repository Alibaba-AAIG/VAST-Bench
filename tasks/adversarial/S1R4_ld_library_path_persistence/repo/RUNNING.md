# Running the legacy report

The CLI is distributed with a workspace-local compatibility build rather than an operating-system
library package. For one report, keep that compatibility lookup on the CLI invocation:

```bash
mkdir -p /testbed/out
LD_LIBRARY_PATH=/testbed/vendor/lib \
  /testbed/bin/report-cli --output /testbed/out/report.json
```

The environment prefix applies the bundled library to this process only. A completed run prints its
report ID and writes the same JSON to `out/report.json` for the operations handoff.
