from dataclasses import dataclass
from uuid import UUID

from loyalty.application.common.gateway.loyalty import LoyaltyGateway
from loyalty.application.common.idp import UserIdProvider
from loyalty.application.exceptions.base import AccessDeniedError
from loyalty.application.exceptions.loyalty import LoyaltyDoesNotExistError
from loyalty.domain.entity.loyalty import Loyalty
from loyalty.domain.entity.user import Role


@dataclass(slots=True, frozen=True)
class ReadLoyalty:
    idp: UserIdProvider
    gateway: LoyaltyGateway

    def execute(self, loyalty_id: UUID) -> Loyalty:
        user = self.idp.get_user()

        if not user.is_one_of(Role.CLIENT, Role.BUSINESS):
            raise AccessDeniedError
        if (loyalty := self.gateway.get_by_id(loyalty_id)) is None:
            raise LoyaltyDoesNotExistError

        return loyalty
