from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from loyalty.domain.entity.user import Role, User


@dataclass
class Business:
    # информация о бизнесе - предприятии которое использует программу лояльности
    business_id: UUID
    name: str
    contact_phone: str | None
    contact_email: str
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))

    def can_read_by(self, user: User) -> bool:
        return user.is_one_of(Role.CLIENT, Role.BUSINESS)
