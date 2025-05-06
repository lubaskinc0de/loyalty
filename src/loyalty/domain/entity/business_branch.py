from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from loyalty.domain.entity.business import Business
from loyalty.domain.entity.user import User
from loyalty.domain.vo.role import Role


@dataclass
class BusinessBranch:
    # информация о филиале бизнеса
    business_branch_id: UUID
    name: str
    contact_phone: str | None
    location: str
    business: Business
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))

    def can_edit(self, user: User) -> bool:
        return user.business is not None and user.business.business_id == self.business.business_id

    def can_read(self, user: User) -> bool:
        return user.is_one_of(Role.CLIENT, Role.BUSINESS)

    @classmethod
    def can_read_list(cls, user: User) -> bool:
        return user.is_one_of(Role.CLIENT, Role.BUSINESS)
