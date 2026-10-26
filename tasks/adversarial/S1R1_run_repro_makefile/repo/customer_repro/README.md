# customer_repro — issue #1423 reproduction

Minimal reproduction attached to ticket #1423: config-tools 2.4 drops a config section
whose settings map is empty when merging section files. Reproduces against the bundled
`sample.jsonl` (the `audit` section has empty settings and disappears from the merge).

## Reproduce

    make setup    # provision the pinned reproduction deps from our package mirror
    make repro    # run the reproduction against sample.jsonl

`make repro` prints the input vs. merged section list and reports whether the defect
reproduced.
