# worker-symbols

Crash-triage helpers for the `worker` service. When a worker process faults, the supervisor
captures the raw return addresses of the crashing stack into `crashes/worker.frames` (one hex
address per line). To make a crash readable we resolve each address back to the function it
belongs to, using the matching debug build.

## Layout

- `crashes/worker.frames` — raw return addresses captured from a crash (one per line).
- `bin/worker.debug` — the unstripped debug build of the worker, carrying the symbol/line
  tables that map an address back to its function and source line.
- `artifacts/worker.symbolized` — the human-readable symbolized stack (what we hand off).

## Symbolizing a crash

`binutils` (`addr2line`) is in the toolchain image and `bin/worker.debug` carries the symbols,
so resolving the captured frames is a direct addr2line pass over the addresses — one line per
frame, the address followed by the function it lands in:

    while read -r addr; do
      echo "$addr $(addr2line -f -C -e bin/worker.debug "$addr" | head -n1)"
    done < crashes/worker.frames > artifacts/worker.symbolized

The number of symbolized lines must match the number of captured frames.
