from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True, frozen=True)
class BusinessPaymentsStats:
    payments_amount: Decimal
    waste_amount: Decimal
    bonus_given_amount: Decimal
