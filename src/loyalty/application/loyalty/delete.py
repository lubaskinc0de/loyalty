from dataclasses import dataclass
from uuid import UUID

from loyalty.application.common.gateway.loyalty import LoyaltyGateway
from loyalty.application.common.idp import BusinessIdProvider
from loyalty.application.common.uow import UoW
from loyalty.application.exceptions.base import AccessDeniedError
from loyalty.application.exceptions.loyalty import LoyaltyDoesNotExistError


@dataclass(slots=True, frozen=True)
class DeleteLoyalty:
    idp: BusinessIdProvider
    gateway: LoyaltyGateway
    uow: UoW

    def execute(self, loyalty_id: UUID) -> None:
        business = self.idp.get_business()
        loyalty = self.gateway.get_by_id(loyalty_id)

        if loyalty is None:
            raise LoyaltyDoesNotExistError

        if not loyalty.can_edit(business):
            raise AccessDeniedError

        self.uow.delete(loyalty)
        self.uow.commit()
