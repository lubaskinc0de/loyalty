from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from loyalty.domain.entity.business import Business


@dataclass
class BusinessBranch:
    # информация о филиале бизнеса
    business_branch_id: UUID
    name: str
    address: str
    contact_phone: str | None
    location: str
    business: Business | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))
