# rowstore

Utilities for the rowstore on-disk row format: size accounting and page-framing
helpers used by the storage engine and its CLI.

## Usage

```rust
use rowstore::format_size;

let human = format_size(2048); // human-readable page size
```

## Releasing

Releases publish the crate to the internal registry through the CI pipeline in
`.ci/pipeline.yml`.
