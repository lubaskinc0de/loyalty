from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from loyalty.domain.vo.role import Role


@dataclass
class Business:
    # информация о бизнесе - предприятии которое использует программу лояльности
    business_id: UUID
    name: str
    contact_phone: str | None
    contact_email: str
    avatar_url: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))

    def can_read_by(self, roles: list[Role]) -> bool:
        return not set(roles).isdisjoint({Role.CLIENT, Role.BUSINESS})
