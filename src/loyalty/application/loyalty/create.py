from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from loyalty.application.common.idp import BusinessIdProvider
from loyalty.application.common.uow import UoW
from loyalty.domain.entity.loyalty import Loyalty
from loyalty.domain.shared_types import Gender


class LoyaltyForm(BaseModel):
    name: str = Field(max_length=100, min_length=2)
    description: str = Field(max_length=3096)
    starts_at: datetime
    ends_at: datetime
    money_per_bonus: int
    min_age: int
    max_age: int
    is_active: bool
    gender: Gender | None = None


@dataclass(slots=True, frozen=True)
class CreateLoyalty:
    uow: UoW
    idp: BusinessIdProvider

    def execute(self, form: LoyaltyForm) -> UUID:
        loyalty_id = uuid4()
        loyalty = Loyalty(
            loyalty_id=loyalty_id,
            name=form.name,
            description=form.description,
            starts_at=form.starts_at,
            ends_at=form.ends_at,
            money_per_bonus=form.money_per_bonus,
            min_age=form.min_age,
            max_age=form.max_age,
            is_active=form.is_active,
            gender=form.gender,
        )

        business = self.idp.get_business()

        self.uow.add(loyalty)
        self.uow.flush((loyalty,))
        loyalty.business = business
        self.uow.commit()

        return loyalty.loyalty_id
