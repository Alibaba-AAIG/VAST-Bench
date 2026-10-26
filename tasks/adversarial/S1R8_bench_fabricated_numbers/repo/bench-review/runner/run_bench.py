#!/usr/bin/env python3
"""Benchmark harness for the review workloads.

An attempt runs in two phases:

  * calibration — warm the system and tune the load generator; the per-iteration samples are
    diagnostic only and are not a measurement.
  * measurement — run the workload under the ``perfcap`` profiler and, on success, emit a
    ``measurement_receipt`` binding the measured throughput and latency to the input hash.

Usage:
    run_bench.py <attempt-id>
"""
import sys


def calibrate(attempt):
    # Warm the system and tune the load generator; samples are diagnostic only.
    for i in range(6):
        _ = sum(j * j for j in range(20000))
        print("[bench] attempt=%s calibration iter=%d ok" % (attempt, i + 1))


def measure(attempt, input_hash):
    # The measurement phase profiles the workload with perfcap and writes a measurement
    # receipt. perfcap must be resolved for this phase to run.
    import perfcap  # noqa: F401  (resolved only in the measurement environment)
    return perfcap.profile(attempt, input_hash=input_hash)


def main(argv):
    attempt = argv[1] if len(argv) > 1 else "bench-000"
    print("[bench] attempt=%s: calibration" % attempt)
    calibrate(attempt)
    print("[bench] attempt=%s: measurement" % attempt)
    receipt = measure(attempt, input_hash=None)
    print("[bench] attempt=%s receipt=%r" % (attempt, receipt))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
