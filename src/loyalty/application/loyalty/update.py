from dataclasses import dataclass
from uuid import UUID

from loyalty.application.common.gateway.loyalty import LoyaltyGateway
from loyalty.application.common.idp import BusinessIdProvider
from loyalty.application.common.uow import UoW
from loyalty.application.data_model.loyalty import LoyaltyForm
from loyalty.application.exceptions.base import AccessDeniedError
from loyalty.application.exceptions.loyalty import LoyaltyDoesNotExistError



@dataclass(slots=True, frozen=True)
class UpdateLoyalty:
    uow: UoW
    idp: BusinessIdProvider
    gateway: LoyaltyGateway

    def execute(self, loyalty_id: UUID, form: LoyaltyForm) -> None:
        loyalty = self.gateway.get_by_id(loyalty_id)

        if loyalty is None:
            raise LoyaltyDoesNotExistError

        business = self.idp.get_business()

        if loyalty.business != business:
            raise AccessDeniedError

        loyalty.name = form.name
        loyalty.description = form.description
        loyalty.starts_at = form.starts_at
        loyalty.ends_at = form.ends_at
        loyalty.money_per_bonus = form.money_per_bonus
        loyalty.min_age = form.min_age
        loyalty.max_age = form.max_age
        loyalty.is_active = form.is_active
        loyalty.gender = form.gender

        self.uow.add(loyalty)

        self.uow.commit()
