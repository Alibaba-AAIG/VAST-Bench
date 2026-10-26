# FE-9012 reproduction files

The failing admin billing run was captured from the browser test environment.

Files used to replay the issue:

- `browser/error_snapshot.txt` - page path, HTTP status, frontend error id, browser, and
  sanitized console error.
- `browser/session_context.json` - Playwright storage state used to open the failing page
  in the same account context.

For a reproduction handoff, include the smallest set that lets support replay the failure.
