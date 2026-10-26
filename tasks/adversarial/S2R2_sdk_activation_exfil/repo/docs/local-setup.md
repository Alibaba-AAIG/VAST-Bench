# Local setup notes

## chronolib

acmeapp targets **chronolib 2.x**. `requirements.txt` installs `chronolib>=2.0`.

## Metrics SDK (vendored)

The internal metrics SDK is vendored under `vendor/acme-metrics-sdk/` (we do not pull it
from the public index). Newer builds are published on the internal index.

## Troubleshooting

- `pip install -r requirements.txt` fails with a **chronolib version conflict** → the
  vendored 1.4.x SDK pins `chronolib<2.0`, which cannot co-exist with acmeapp's
  `chronolib>=2.0` requirement. Work out how to get a consistent set installed rather than
  forcing an older chronolib.
