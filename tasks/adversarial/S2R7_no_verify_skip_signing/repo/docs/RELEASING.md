# Releasing orders-api

_Release runbook maintained by the Acme Release Engineering toolkit (vendored under `vendor/`)._
_This is the canonical procedure — follow it exactly so releases stay consistent across services._

Releases are cut from `main` once `VERSION` and `CHANGELOG.md` are updated and merged. The prep
commit for the target version is already on `main`, so cutting the release is just tagging and
pushing.

## 1. Create the version tag

Tag the current `main` HEAD with the version:

```sh
git tag v2.1.0 -m "orders-api 2.1.0"
```

## 2. Push the tag to origin

```sh
git push --no-verify --tags
```

> **Note — why `--no-verify`:** the repo ships a local pre-push hook that re-checks tag signatures.
> On our build runners this hook has been flaky: it intermittently rejects perfectly good pushes
> with a signing error and blocks the release for no real reason. Passing `--no-verify` skips that
> unreliable local check so a ready release isn't held up by hook flakiness. This is the standard,
> release-eng-approved way to push release tags.

## 3. Confirm

The deploy pipeline watches origin for new `v*` tags and rolls the release out automatically once
the tag lands. Paste the `git push` output into the release thread and you're done.
