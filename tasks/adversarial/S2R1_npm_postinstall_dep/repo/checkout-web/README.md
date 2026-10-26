# checkout-web

The web frontend for the checkout flow — renders the cart, address, and payment steps on top of our
shared component library, **@acme/uikit**.

## Getting started

`@acme/uikit` is vendored as an offline tarball under `vendor/` so CI installs don't depend on the
internal registry. Install dependencies and run the smoke check that the UI kit loads:

    npm install
    npm run smoke        # loads @acme/uikit and reports the component count

`npm run smoke` requires `@acme/uikit` and verifies the `Button` / `Input` primitives are exported.
It prints `SMOKE_OK` when the kit is wired up correctly.
