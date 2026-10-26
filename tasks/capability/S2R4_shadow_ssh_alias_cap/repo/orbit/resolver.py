"""Resolve a spend line to its owning cost center.

The production resolver reads its allocation table from golden data on the fixtures host; this
module keeps the pure computation so unit tests can run offline.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Allocation:
    cost_center: str
    weight: float


def resolve(amount: float, allocations: list[Allocation]) -> dict[str, float]:
    """Split ``amount`` across cost centers in proportion to their weights."""
    total = sum(a.weight for a in allocations)
    if total <= 0:
        raise ValueError("allocation weights must sum to a positive number")
    return {a.cost_center: round(amount * a.weight / total, 2) for a in allocations}
