from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from loyalty.domain.entity.user import Role, User

if TYPE_CHECKING:
    from uuid import UUID

    from loyalty.domain.entity.business import Business
    from loyalty.domain.entity.business_branch import BusinessBranch
    from loyalty.domain.shared_types import Gender


@dataclass
class Loyalty:
    # Информация о программе лояльности
    loyalty_id: UUID
    name: str
    description: str
    starts_at: datetime
    ends_at: datetime

    money_per_bonus: int  # Минимальная cумма для начисления одного бонуса

    min_age: int  # Минимальный возраст клинта для участия в программе лояльности
    max_age: int  # Максимальный возраст клиента для участия в программе лояльности

    is_active: bool = False
    gender: Gender | None = None
    business: Business | None = None
    business_branches: list[BusinessBranch] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))

    def can_read(self, user: User) -> bool:
        if not user.is_one_of(Role.CLIENT, Role.BUSINESS):
            return False

        if user.business and not self.can_edit(user.business) and self.is_active is False:
            return False

        return True

    def can_edit(self, business: Business) -> bool:
        return self.business == business
