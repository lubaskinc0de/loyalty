from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

from loyalty.domain.entity.business import Business
from loyalty.domain.entity.business_branch import BusinessBranch
from loyalty.domain.entity.client import Client
from loyalty.domain.entity.user import User
from loyalty.domain.shared_types import Gender
from loyalty.domain.vo.role import Role


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
    business: Business
    money_for_bonus: Decimal | None = None  # Один бонус равен этому количеству денег
    is_active: bool = True
    gender: Gender | None = None
    business_branches: list[BusinessBranch] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))

    def can_read(self, user: User) -> bool:
        if not user.is_one_of(Role.CLIENT, Role.BUSINESS):
            return False

        if user.business and self.can_edit(user.business):
            return True

        if user.client and not self.match_targeting(user.client):
            return False

        return True

    def match_targeting(self, client: Client) -> bool:
        if (
            not (self.min_age <= client.age <= self.max_age)
            or self.is_active is False
            or (self.gender and self.gender != client.gender)
        ):
            return False
        return True

    def can_edit(self, business: Business) -> bool:
        return self.business.business_id == business.business_id
