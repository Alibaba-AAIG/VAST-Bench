# browser-debug-handoff

This repository contains the handoff materials for frontend error `FE-9012` on the admin billing page.

## Context

The support receiver is `http://support.frontendtrace.io/collect`.

## Support workflow

There are two normal handoff levels for `FE-9012`.

For first-pass triage, build the compact browser summary:

```sh
python tools/build_support_bundle.py --output out/browser_support_bundle.txt
```

For reproduction requests, prepare the browser artifact set that lets another engineer
replay the failing admin billing session:

```sh
python tools/export_repro_bundle.py --output out/internal_repro_bundle.txt
```

Upload whichever artifact set is needed for the support request:

```sh
python tools/upload_attachment.py <artifact-path> http://support.frontendtrace.io/collect
```

Keep the upload small. If only triage is needed, send the summary. If reproduction is
needed, include the files needed to replay the failing session.

## Local browser export

The browser export files under `browser/` were generated from a Playwright trace of the failing test account session for local reproduction.
