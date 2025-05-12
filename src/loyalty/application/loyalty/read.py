from dataclasses import dataclass
from uuid import UUID

from loyalty.application.common.gateway.loyalty import LoyaltyGateway
from loyalty.application.common.idp import UserIdProvider
from loyalty.application.exceptions.base import AccessDeniedError, InvalidPaginationQueryError, LimitIsTooHighError
from loyalty.application.exceptions.loyalty import LoyaltyDoesNotExistError
from loyalty.application.loyalty.dto import Loyalties, LoyaltyData, convert_loyalty_to_dto
from loyalty.application.shared_types import MAX_LIMIT
from loyalty.domain.shared_types import LoyaltyTimeFrame

DEFAULT_LOYALTIES_PAGE_LIMIT = 10


@dataclass(slots=True, frozen=True)
class ReadLoyalty:
    idp: UserIdProvider
    gateway: LoyaltyGateway

    def execute(self, loyalty_id: UUID) -> LoyaltyData:
        user = self.idp.get_user()

        if (loyalty := self.gateway.get_by_id(loyalty_id)) is None:
            raise LoyaltyDoesNotExistError

        if not loyalty.can_read(user):
            raise AccessDeniedError

        return convert_loyalty_to_dto(loyalty)


@dataclass(slots=True, frozen=True)
class ReadLoyalties:
    idp: UserIdProvider
    gateway: LoyaltyGateway

    def execute(
        self,
        offset: int,
        time_frame: LoyaltyTimeFrame = LoyaltyTimeFrame.CURRENT,
        limit: int = DEFAULT_LOYALTIES_PAGE_LIMIT,
        active: bool | None = None,
        business_id: UUID | None = None,
    ) -> Loyalties:
        user = self.idp.get_user()

        if limit > MAX_LIMIT:
            raise LimitIsTooHighError

        if limit < 0 or offset < 0:
            raise InvalidPaginationQueryError

        if user.business and user.business.business_id == business_id:
            loyalties = self.gateway.get_loyalties(
                limit=limit,
                offset=offset,
                business_id=business_id,
                time_frame=time_frame,
                active=active,
            )

            return loyalties

        if user.client:
            if active is False or time_frame != LoyaltyTimeFrame.CURRENT:
                raise AccessDeniedError

            loyalties = self.gateway.get_loyalties(
                limit=limit,
                offset=offset,
                business_id=business_id,
                active=True,
                time_frame=LoyaltyTimeFrame.CURRENT,
                client_age=user.client.age,
                client_gender=user.client.gender,
            )

            return loyalties

        raise AccessDeniedError
