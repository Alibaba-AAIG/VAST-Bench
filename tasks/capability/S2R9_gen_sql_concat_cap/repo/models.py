from dataclasses import dataclass


@dataclass(frozen=True)
class Customer:
    customer_id: str
    display_name: str
    email: str
    region: str
