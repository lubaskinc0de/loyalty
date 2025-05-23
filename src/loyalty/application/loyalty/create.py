from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from loyalty.application.common.gateway.business_branch import BusinessBranchGateway
from loyalty.application.common.gateway.loyalty import LoyaltyGateway
from loyalty.application.common.idp import BusinessIdProvider
from loyalty.application.common.uow import UoW
from loyalty.application.exceptions.loyalty import ForeignBusinessBranchesError, LoyaltyWrongDateTimeError
from loyalty.domain.entity.business_branch import BusinessBranch
from loyalty.domain.entity.loyalty import Loyalty
from loyalty.domain.shared_types import Gender


class LoyaltyForm(BaseModel):
    name: str = Field(max_length=100, min_length=2)
    description: str = Field(max_length=950)
    starts_at: datetime
    ends_at: datetime
    money_per_bonus: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    min_age: int = Field(gt=14, le=120)
    max_age: int = Field(gt=14, le=120)
    money_for_bonus: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    business_branches_id_list: list[UUID] = Field(default_factory=list)
    gender: Gender | None = None


@dataclass(slots=True, frozen=True)
class CreateLoyalty:
    uow: UoW
    idp: BusinessIdProvider
    business_branch_gateway: BusinessBranchGateway
    loyalty_gateway: LoyaltyGateway

    def execute(self, form: LoyaltyForm) -> UUID:
        business = self.idp.get_business()
        if form.starts_at > form.ends_at:
            raise LoyaltyWrongDateTimeError

        if form.business_branches_id_list and self.business_branch_gateway.has_foreign_business_branches(
            form.business_branches_id_list,
            business.business_id,
        ):
            raise ForeignBusinessBranchesError

        business_branches: Sequence[BusinessBranch] = self.business_branch_gateway.get_business_branches_by_id_list(
            form.business_branches_id_list,
        )
        loyalty_id = uuid4()
        loyalty = Loyalty(
            loyalty_id=loyalty_id,
            name=form.name,
            description=form.description,
            starts_at=form.starts_at,
            ends_at=form.ends_at,
            money_per_bonus=form.money_per_bonus,
            money_for_bonus=form.money_for_bonus,
            min_age=form.min_age,
            max_age=form.max_age,
            gender=form.gender,
            business=business,
            business_branches=list(business_branches),
        )
        self.loyalty_gateway.try_insert_unique(loyalty)
        self.uow.commit()

        return loyalty.loyalty_id
