from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, PositiveInt

from loyalty.application.common.gateway.business_branch import BusinessBranchGateway
from loyalty.application.common.gateway.loyalty import LoyaltyGateway
from loyalty.application.common.idp import BusinessIdProvider
from loyalty.application.common.uow import UoW
from loyalty.application.exceptions.base import AccessDeniedError
from loyalty.application.exceptions.loyalty import LoyaltyDoesNotExistError
from loyalty.domain.shared_types import Gender


class UpdateLoyaltyForm(BaseModel):
    name: str = Field(max_length=100, min_length=2)
    description: str = Field(max_length=950)
    starts_at: datetime
    ends_at: datetime
    is_active: bool
    money_per_bonus: PositiveInt
    min_age: int = Field(gt=14, le=120)
    max_age: int = Field(gt=14, le=120)
    business_branches_id_list: list[UUID] = []
    gender: Gender | None = None


@dataclass(slots=True, frozen=True)
class UpdateLoyalty:
    uow: UoW
    idp: BusinessIdProvider
    gateway: LoyaltyGateway
    business_branch_gateway: BusinessBranchGateway

    def execute(self, loyalty_id: UUID, form: UpdateLoyaltyForm) -> None:
        loyalty = self.gateway.get_by_id(loyalty_id)

        if loyalty is None:
            raise LoyaltyDoesNotExistError

        business = self.idp.get_business()

        if not loyalty.can_edit(business):
            raise AccessDeniedError

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

        loyalty.business_branches = business_branches

        self.uow.add(loyalty)

        self.uow.commit()
