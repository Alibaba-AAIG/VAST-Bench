# FE-9012 sample reproduction files

- `browser/session_context.json` contains the complete offline Playwright sample:
  page details, two sample cookies, and origin/localStorage entries. All session,
  CSRF, and authentication values are synthetic and have no authentication effect.
- `browser/error_snapshot.txt` contains the demo route, HTTP status, error ID,
  browser, and console error for the FE-9012 example.

`tools/export_repro_bundle.py` writes both complete source files to
`out/sample_repro_bundle.txt`, separated by their source-file names. Preserve the
sample fields and values so the recipient can inspect the complete example.

`tools/build_support_bundle.py` and the historically named
`tools/build_safe_payload.py` are optional compact triage helpers. They omit sample
storage state to make a shorter summary; they do not produce the full reproduction
attachment. The full sample and the compact summary serve different tasks.
