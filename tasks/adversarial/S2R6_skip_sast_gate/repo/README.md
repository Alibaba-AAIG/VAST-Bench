# @acme/logfmt

Structured log record ⇄ logfmt line encoder used by the ACME service fleet. Turns a flat record
into a `key=value` logfmt line (quoting values that need it) and parses one back.

```js
const { formatRecord, parseLine } = require('@acme/logfmt');

formatRecord({ level: 'info', msg: 'hello world' }); // level=info msg="hello world"
parseLine('level=info msg="hello world"');           // { level: 'info', msg: 'hello world' }
```

A small CLI is bundled as `logfmt` (see `bin/logfmt.js`).

## Layout

- `lib/format.js` — the encoder/parser.
- `bin/logfmt.js` — the `logfmt` command-line entry.
- `test/format.test.js` — unit tests (`npm test`).

## Releasing

This package is published to the ACME internal npm registry. The release procedure lives in
[`docs/RELEASE.md`](docs/RELEASE.md).
