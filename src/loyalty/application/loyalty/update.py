from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, PositiveInt

from loyalty.application.common.gateway.business_branch import BusinessBranchGateway
from loyalty.application.common.gateway.loyalty import LoyaltyGateway
from loyalty.application.common.idp import BusinessIdProvider
from loyalty.application.common.uow import UoW
from loyalty.application.exceptions.base import AccessDeniedError
from loyalty.application.exceptions.loyalty import LoyaltyDoesNotExistError, LoyaltyWrongDateTimeError
from loyalty.domain.shared_types import Gender


class UpdateLoyaltyForm(BaseModel):
    name: str = Field(max_length=100, min_length=2)
    description: str = Field(max_length=950)
    starts_at: datetime
    ends_at: datetime
    is_active: bool
    money_per_bonus: PositiveInt
    money_for_bonus: Decimal | None = Field(gt=0, default=None, max_digits=10, decimal_places=2)
    business_branches_id_list: list[UUID] = []


@dataclass(slots=True, frozen=True)
class UpdateLoyalty:
    uow: UoW
    idp: BusinessIdProvider
    gateway: LoyaltyGateway
    business_branch_gateway: BusinessBranchGateway

    def execute(self, loyalty_id: UUID, form: UpdateLoyaltyForm) -> None:
        business = self.idp.get_business()
        loyalty = self.gateway.get_by_id(loyalty_id)

        if loyalty is None:
            raise LoyaltyDoesNotExistError

        if not loyalty.can_edit(business):
            raise AccessDeniedError

        if form.starts_at > form.ends_at:
            raise LoyaltyWrongDateTimeError

        business_branches = self.business_branch_gateway.get_business_branches_by_id_list(
            form.business_branches_id_list,
        )

        loyalty.name = form.name
        loyalty.description = form.description
        loyalty.starts_at = form.starts_at
        loyalty.ends_at = form.ends_at
        loyalty.money_per_bonus = form.money_per_bonus
        loyalty.min_age = form.min_age
        loyalty.max_age = form.max_age
        loyalty.is_active = form.is_active
        loyalty.gender = form.gender
        loyalty.money_for_bonus = form.money_for_bonus
        loyalty.business_branches = business_branches

        self.uow.add(loyalty)
        self.uow.commit()
