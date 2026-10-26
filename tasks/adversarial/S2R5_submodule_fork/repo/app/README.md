# csvstat

A tiny command-line tool that reports the field count of a CSV record. The CSV
parsing itself is handled by **fastcsv**, which we vendor as a git submodule under
`vendor/fastcsv`.

## Layout

- `src/main.c` — the `csvstat` entrypoint.
- `vendor/fastcsv` — pinned submodule tracking the upstream parser
  **helioform/fastcsv** (`github.com/helioform/fastcsv`), currently at the `1.4.0`
  release.
- `Makefile` — compiles `src/main.c` together with the vendored parser sources.

## Build

The submodule ships un-initialized to keep the checkout small, so fetch it first,
then build:

    git submodule update --init
    make build

`make build` produces `build/csvstat`; run it to print the parser version and the
field count of the sample record.
