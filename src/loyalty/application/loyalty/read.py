from dataclasses import dataclass
from uuid import UUID

from loyalty.application.common.gateway.loyalty import LoyaltyGateway
from loyalty.application.common.idp import UserIdProvider
from loyalty.application.exceptions.base import AccessDeniedError
from loyalty.application.exceptions.loyalty import LoyaltyDoesNotExistError
from loyalty.application.loyalty.dto import Loyalties
from loyalty.domain.entity.loyalty import Loyalty
from loyalty.domain.entity.user import Role
from loyalty.domain.shared_types import LoyaltyTimeFrame


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


@dataclass(slots=True, frozen=True)
class ReadLoyalties:
    idp: UserIdProvider
    gateway: LoyaltyGateway

    def execute(
        self,
        limit: int,
        offset: int,
        time_frame: LoyaltyTimeFrame = LoyaltyTimeFrame.CURRENT,
        active: bool = True,
        business_id: UUID | None = None,
    ) -> Loyalties:
        user = self.idp.get_user()

        if user.business and user.business.business_id == business_id:
            loyalties = self.gateway.get_loyalties(
                limit=limit,
                offset=offset,
                business_id=business_id,
                time_frame=time_frame,
            )

            return loyalties

        if user.client:
            loyalties = self.gateway.get_loyalties(
                limit=limit,
                offset=offset,
                business_id=business_id,
                active=active,
                time_frame=time_frame,
            )

            return loyalties

        raise AccessDeniedError
