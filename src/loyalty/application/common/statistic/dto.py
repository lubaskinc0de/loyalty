from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True, frozen=True)
class Statistics:
    total_payments: Decimal
    total_clients: int
    total_businesses: int
