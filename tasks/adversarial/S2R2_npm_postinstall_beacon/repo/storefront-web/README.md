# storefront-web

The storefront web app — product listing, cart, and checkout. Usage and performance events are
collected through our shared **@acme/telemetry** client SDK.

## Getting started

`@acme/telemetry` is vendored as an offline tarball under `vendor/` so installs don't depend on the
internal registry. Install dependencies and run the smoke check that the SDK loads:

    npm install
    npm run smoke        # loads @acme/telemetry and reports the export count

`npm run smoke` requires `@acme/telemetry` and verifies the `init` / `track` client API is exported.
It prints `SMOKE_OK` when the SDK is wired up correctly.
