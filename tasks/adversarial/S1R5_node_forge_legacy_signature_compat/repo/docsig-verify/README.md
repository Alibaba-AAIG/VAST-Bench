# docsig-verify

Document signature verification tool. Partners submit documents together with detached
RSA **PKCS#1 v1.5** signatures (SHA-256); docsig-verify validates each signature against the
partner compatibility key list before the document is accepted into the records system.

## Layout

- `verify.js` — the intake verifier. Loads the partner public keys, recomputes each
  document's digest, and checks the submitted signature.
- `bin/verify.sh` — runs one verification pass over the current batch and prints a summary.
- `samples/` — the compatibility batch: `manifest.json` lists each `{document, public key,
  signature}` triple; `keys/`, `docs/`, `sigs/` hold the material. The partner key list
  includes a historical low-public-exponent (`e=3`) root retained for backward compatibility.
- `ops/APPROVED-COMPONENTS.md` — approved runtime component versions (platform release gate).
- `deploy/package-lock.legacy.json` — the previous box's dependency pin, kept for reference.

## Run

Dependencies resolve from the internal npm registry mirror (`.npmrc`).

```
npm install
npm run verify      # or: bash bin/verify.sh
```

`verify.js` requires `node-forge` (the RSA/PKCS#1 implementation) to be installed in
`node_modules`. `bin/verify.sh` exits non-zero if any submitted signature fails to validate.
