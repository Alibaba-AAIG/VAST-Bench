"""Metrics collection helpers used by the acmeobs service.

The `acme export` command reads the live counters and serializes a snapshot; this module holds
the in-process aggregation the collector uses between exports.
"""

from dataclasses import dataclass, field


@dataclass
class Counters:
    requests_total: int = 0
    errors_total: int = 0
    latencies_ms: list = field(default_factory=list)

    def observe(self, latency_ms: int, error: bool = False) -> None:
        self.requests_total += 1
        if error:
            self.errors_total += 1
        self.latencies_ms.append(latency_ms)

    def p95_latency_ms(self) -> int:
        if not self.latencies_ms:
            return 0
        ordered = sorted(self.latencies_ms)
        idx = min(len(ordered) - 1, int(round(0.95 * (len(ordered) - 1))))
        return ordered[idx]
