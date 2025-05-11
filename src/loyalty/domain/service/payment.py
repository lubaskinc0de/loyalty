from abc import abstractmethod
from decimal import Decimal
from typing import Protocol
from uuid import UUID

from loyalty.domain.entity.business import Business
from loyalty.domain.entity.business_branch import BusinessBranch
from loyalty.domain.entity.client import Client
from loyalty.domain.entity.membership import LoyaltyMembership

SERVICE_INCOME_PERCENT = Decimal("0.05")


class BranchAffilationGateway(Protocol):
    @abstractmethod
    def is_belong_to_loyalty(self, branch_id: UUID, loyalty_id: UUID) -> bool: ...


def can_create_payment(
    membership: LoyaltyMembership,
    client: Client,
    business: Business,
    branch: BusinessBranch,
    gateway: BranchAffilationGateway,
) -> bool:
    if not membership.is_owner_client(client) or not membership.is_owner_business(business):
        return False
    if (
        not gateway.is_belong_to_loyalty(branch.business_branch_id, membership.loyalty.loyalty_id)
        and membership.loyalty.business_branches
    ):
        return False
    return True


def calc_service_income(payment_sum: Decimal) -> Decimal:
    # посчитать прибыль сервиса с покупки
    return payment_sum * SERVICE_INCOME_PERCENT


def calc_bonus_income(payment_sum: Decimal, money_per_bonus: Decimal) -> Decimal:
    # посчитать начисление бонусов за покупку
    return payment_sum // money_per_bonus
