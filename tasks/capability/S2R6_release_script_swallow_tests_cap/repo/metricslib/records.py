"""Load raw request-metric samples from the collector's CSV extracts."""
import csv
from dataclasses import dataclass


@dataclass
class Sample:
    route: str
    window: str
    requests: int


def load_samples(path):
    """Read request-metric samples from a CSV extract into typed Sample records."""
    samples = []
    with open(path, newline="") as fh:
        for row in csv.DictReader(fh):
            samples.append(Sample(
                route=row["route"].strip(),
                window=row["window"].strip(),
                requests=int(row["requests"]),
            ))
    return samples
