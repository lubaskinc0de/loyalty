from decimal import Decimal

from loyalty.domain.common.affilation import BranchAffilationGateway
from loyalty.domain.entity.business import Business
from loyalty.domain.entity.business_branch import BusinessBranch
from loyalty.domain.entity.client import Client
from loyalty.domain.entity.membership import LoyaltyMembership

SERVICE_INCOME_PERCENT = Decimal("0.05")
BONUS_BALANCE_COEF = Decimal("0.08")  # процент на остаток


def can_create_payment(
    membership: LoyaltyMembership,
    client: Client,
    business: Business,
    branch: BusinessBranch,
    gateway: BranchAffilationGateway,
) -> bool:
    if not membership.is_owner_client(client) or not membership.is_owner_business(business):
        return False

    loyalty = membership.loyalty
    if not loyalty.is_belong_to(branch, gateway):
        return False

    return True


def calc_service_income(payment_sum: Decimal) -> Decimal:
    # посчитать прибыль сервиса с покупки
    return payment_sum * SERVICE_INCOME_PERCENT


def calc_bonus_income(payment_sum: Decimal, money_per_bonus: Decimal, bonus_balance: Decimal) -> Decimal:
    # посчитать начисление бонусов за покупку
    return (payment_sum // money_per_bonus) + (bonus_balance * BONUS_BALANCE_COEF)
