# @acme/uikit

ACME's internal TypeScript UI component library — small, dependency-free helpers and
component descriptors shared across the app teams.

## Layout

- `src/` — the library source (TypeScript).
- `Makefile` — build + release automation.

## Development

```bash
make lint        # eslint over src/
make typecheck   # tsc --noEmit
```

## Release

Cut a release to the internal npm registry with:

```bash
make release
```

which runs the lint and typecheck gates and publishes `@acme/uikit` to the registry
configured in `.npmrc`.
