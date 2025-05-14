from dataclasses import dataclass
from uuid import UUID

from loyalty.application.business.dto import Businesses
from loyalty.application.common.gateway.business import BusinessGateway
from loyalty.application.common.idp import UserIdProvider
from loyalty.application.exceptions.base import AccessDeniedError, InvalidPaginationQueryError, LimitIsTooHighError
from loyalty.application.exceptions.business import BusinessDoesNotExistError
from loyalty.application.shared_types import MAX_LIMIT
from loyalty.domain.entity.business import Business


DEFAULT_BUSINESSES_PAGE_LIMIT = 5


@dataclass(slots=True, frozen=True)
class ReadBusiness:
    idp: UserIdProvider
    gateway: BusinessGateway

    def execute(self, business_id: UUID) -> Business:
        user = self.idp.get_user()
        if (business := self.gateway.get_by_id(business_id)) is None:
            raise BusinessDoesNotExistError

        if not business.can_read_by(user.available_roles):
            raise AccessDeniedError

        return business


@dataclass(slots=True, frozen=True)
class ReadBusinesses:
    idp: UserIdProvider
    gateway: BusinessGateway

    def execute(self, offset: int, limit: int = DEFAULT_BUSINESSES_PAGE_LIMIT) -> Businesses:
        if limit > MAX_LIMIT or offset > MAX_LIMIT:
            raise LimitIsTooHighError

        if limit < 0 or offset < 0:
            raise InvalidPaginationQueryError

        businesses = self.gateway.get_businesses(
            limit=limit,
            offset=offset,
        )
        return businesses