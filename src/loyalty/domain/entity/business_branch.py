from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from loyalty.domain.entity.business import Business


@dataclass
class BusinessBranch:
    # информация о филиале бизнеса
    business_branch_id: UUID
    name: str
    contact_phone: str | None
    location: str
    business: Business | None = None
    loyalties: list["Loyalty"] = field(default_factory=list)  # type: ignore
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))
