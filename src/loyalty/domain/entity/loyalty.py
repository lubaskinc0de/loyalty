from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

from loyalty.domain.common.affilation import BranchAffilationGateway
from loyalty.domain.entity.business import Business
from loyalty.domain.entity.business_branch import BusinessBranch
from loyalty.domain.entity.client import Client
from loyalty.domain.entity.user import User
from loyalty.domain.shared_types import Gender
from loyalty.domain.vo.role import Role

MAX_DISCOUNT = Decimal("0.75")


@dataclass
class Loyalty:
    # Информация о программе лояльности
    loyalty_id: UUID
    name: str
    description: str
    starts_at: datetime
    ends_at: datetime
    money_per_bonus: Decimal  # Минимальная cумма для начисления одного бонуса
    min_age: int  # Минимальный возраст клинта для участия в программе лояльности
    max_age: int  # Максимальный возраст клиента для участия в программе лояльности
    business: Business
    money_for_bonus: Decimal  # Один бонус равен этому количеству денег
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
            or self.starts_at > datetime.now(tz=UTC)
            or self.ends_at < datetime.now(tz=UTC)
        ):
            return False
        return True

    def can_edit(self, business: Business) -> bool:
        return self.business.business_id == business.business_id

    def is_belong_to(self, branch: BusinessBranch, gateway: BranchAffilationGateway) -> bool:
        return gateway.is_belong_to_loyalty(branch_id=branch.business_branch_id, loyalty_id=self.loyalty_id) or (
            not bool(self.business_branches)
        )

    def apply_discount(
        self,
        purchase_amount: Decimal,
        bonus_balance: Decimal,
    ) -> tuple[Decimal, Decimal]:
        """Рассчитывает сумму покупки с учетом бонусов клиента и настроек программы лояльности.
        А также возвращает вторым элементом кол-во потраченных бонусов.
        """
        max_discount = purchase_amount * MAX_DISCOUNT
        potential_discount = bonus_balance * self.money_for_bonus

        actual_discount = min(potential_discount, max_discount)
        used_bonuses = actual_discount / self.money_for_bonus
        new_amount = purchase_amount - actual_discount

        return new_amount.quantize(Decimal(".01")), used_bonuses.quantize(Decimal(".01"))
