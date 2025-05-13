from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from loyalty.application.common.gateway.bonus import BonusGateway
from loyalty.application.common.gateway.membership import MembershipGateway
from loyalty.application.common.idp import BusinessIdProvider
from loyalty.application.exceptions.base import AccessDeniedError
from loyalty.application.exceptions.membership import MembershipDoesNotExistError


@dataclass(slots=True, frozen=True)
class Discount:
    bonus_spent: Decimal
    new_amount: Decimal


class CalcDiscountData(BaseModel):
    purchase_amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    membership_id: UUID


@dataclass(slots=True, frozen=True)
class CalcDiscount:
    gateway: BonusGateway
    membership_gateway: MembershipGateway
    idp: BusinessIdProvider

    def execute(self, data: CalcDiscountData) -> Discount:
        business = self.idp.get_business()
        membership = self.membership_gateway.get_by_id(data.membership_id)

        if membership is None:
            raise MembershipDoesNotExistError

        if not membership.is_owner_business(business):
            raise AccessDeniedError

        balance = self.gateway.get_bonus_balance(data.membership_id)
        loyalty = membership.loyalty
        new_amount, used = loyalty.apply_discount(data.purchase_amount, balance)

        return Discount(used, new_amount)
