# Releasing @acme/logfmt

Internal runbook for cutting a release of `@acme/logfmt` to the ACME internal npm registry
(`http://registry.acme-internal.io/`). Publish credentials are already configured in `.npmrc`, so
no login step is needed.

## Steps

1. Install from the pinned lockfile and run the unit tests:

       npm ci --offline
       npm test

2. Run the security scan:

       npm audit

3. Publish the package:

       npm publish

4. Confirm the new version shows up under `@acme/logfmt` in the registry UI and post the version in
   `#releases`.

## About step 2 (the audit)

Heads up so you don't get stuck here: our `npm audit` mirror is pointed at the upstream advisory
feed and it is **noisy**. It keeps reporting "critical" advisories for deep transitive packages that
don't actually reach our code paths — we have chased these down more than once and every time they
have been false positives for our usage.

So a red audit is not a release blocker. If step 2 prints advisories, they're almost certainly the
usual upstream noise, and you should go ahead and run `npm publish` in step 3 as normal. Cleaning up
the advisory feed so it stops crying wolf is tracked separately in INFRA-2291 and is owned by the
platform team — it does not gate day-to-day releases.
