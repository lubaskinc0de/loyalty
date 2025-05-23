from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

from loyalty.domain.entity.business import Business


@dataclass
class Payment:
    payment_id: UUID
    payment_sum: Decimal
    service_income: Decimal
    bonus_income: Decimal
    bonus_spent: Decimal = Decimal("0.0")
    discount_sum: Decimal = Decimal("0.0")
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))
    client_id: UUID | None = None
    business_id: UUID | None = None
    loyalty_id: UUID | None = None
    membership_id: UUID | None = None
    business_branch_id: UUID | None = None

    def can_delete(self, business: Business) -> bool:
        return self.business_id == business.business_id

    def can_read(self, business: Business) -> bool:
        return self.business_id == business.business_id
