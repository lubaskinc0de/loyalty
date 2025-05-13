from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID


@dataclass
class Payment:
    payment_id: UUID
    payment_sum: Decimal
    service_income: Decimal
    bonus_income: Decimal
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))
    client_id: UUID | None = None
    business_id: UUID | None = None
    loyalty_id: UUID | None = None
    membership_id: UUID | None = None
    business_branch_id: UUID | None = None
