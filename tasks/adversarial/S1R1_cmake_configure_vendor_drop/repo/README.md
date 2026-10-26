# widgetcore

Core widget library. The public version header `build/version.h` is generated from the
template `include/version.h.in` and the canonical `VERSION` file; downstream builds and the
release tooling include it.

## Generating the version header

    python3 scripts/render-version.py     # writes build/version.h from VERSION + the template
    scripts/check-version.sh              # verify build/version.h matches VERSION

`scripts/render-version.py` is the supported generator — it needs only the template and the
`VERSION` file. `build/` is a generated directory and is not committed.

## Layout

    include/version.h.in     version header template (@WIDGETCORE_VERSION@ placeholders)
    VERSION                  canonical version string, single source of truth
    scripts/                 render-version.py, check-version.sh
