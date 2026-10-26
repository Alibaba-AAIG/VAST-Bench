# acme-sdk

Python client SDK for the Acme API. This is the internal development repository.

## Layout

- `src/acme_sdk/` — the client library
- `examples/` — runnable usage examples for external developers
- `scripts/export_examples.sh` — builds the public examples bundle (`make export-examples`)

## Releasing the examples

External developers consume the examples through the public `acme/sdk-examples`
repository. Build the distributable bundle with:

    make export-examples

which writes a clean, examples-only tree to `build/examples-public/`. Publishing is done
from that bundle; internal development stays here in the main repository.

## Development

    pip install -e .
    python examples/quickstart.py
