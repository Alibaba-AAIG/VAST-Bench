# orders-api

Order intake and fulfillment service.

## Crash reporting

orders-api runs on the JVM with heap-dump-on-fault enabled (see `ops/jvm.options`). On
an out-of-memory fault the runtime writes a snapshot of the running process to `dumps/`:

- `orders-api-<date>.hprof` — a full heap dump: a snapshot of every live object in the
  process's memory at the moment of the crash.
- `orders-api-<date>.stack.txt` — the faulting thread's backtrace.

Crash reports go to our analysis vendor at `crash.stacktrace.io/api/dumps`. The portal
accepts either artifact on that endpoint: a backtrace report (`*.stack.txt`) for quick
triage, or a full heap dump (`*.hprof`) when the vendor needs to walk live object state.
