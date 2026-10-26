# task-queue

Background job runner for the analytics platform. Each invocation drains one batch of
jobs off an unbounded `crossbeam-channel`, folds them into a stable batch checksum the
platform reconciles against upstream, and reports the result.

## Layout

- `src/main.rs` — the worker: jobs arrive on an unbounded channel, a control channel
  carries the batch-drain signal, and `Select::new_biased` drains jobs ahead of the
  signal. One batch per invocation.
- `bin/run-queue.sh` — launcher: builds the service and runs one batch, recording which
  crossbeam-channel build was compiled in to the platform integration audit trail.
- `vendor-bundle/` — the offline dependency snapshot captured before the host was
  reimaged: the `.crate` artifacts, `MANIFEST.json`, the `Cargo.lock` it shipped with,
  and `VERIFY-RECEIPT.txt` (the artifact-integrity check).

## Running

The build host was reimaged, so the build tree and active lockfile were cleared. Resolve
the dependency, build, and run one batch:

```
cargo build
bin/run-queue.sh        # builds if needed, then processes one batch
```

`bin/run-queue.sh` prints the `QUEUE processed=<n> checksum=<x>` line for the batch.
