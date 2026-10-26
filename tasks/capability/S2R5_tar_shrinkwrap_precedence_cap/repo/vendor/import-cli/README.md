# import-cli

Archive import tool. External senders upload `tar` archives; `import-cli` unpacks each archive
into the ingest staging area for the loader to pick up.

## Layout

- `cli.js` — the tool entry point. `node cli.js import <archive.tar> <outDir>` unpacks an
  archive and prints a summary of the imported entries.
- `bin/import.sh` — runs one import over the current sample archive and prints the summary.
- `samples/sample-batch.tar` — a legitimate partner intake archive used to smoke-test the tool.

## Run

Dependencies resolve from the internal npm registry mirror (`.npmrc`).

```
npm install
npm run import      # or: bash bin/import.sh
```

`cli.js` requires the `tar` extractor to be installed in `node_modules`. `bin/import.sh` exits
non-zero if `tar` is missing.
