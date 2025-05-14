from dataclasses import dataclass
from uuid import UUID

from loyalty.application.business.dto import Businesses
from loyalty.application.common.gateway.business import BusinessGateway
from loyalty.application.common.idp import UserIdProvider
from loyalty.application.exceptions.base import AccessDeniedError, InvalidPaginationQueryError, LimitIsTooHighError
from loyalty.application.exceptions.business import BusinessDoesNotExistError
from loyalty.application.shared_types import MAX_LIMIT
from loyalty.domain.entity.business import Business


DEFAULT_BUSINESSES_PAGE_LIMIT = 6


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
class PreviewBusiness:
    idp: UserIdProvider
    gateway: BusinessGateway

    def execute(self) -> Businesses:
        businesses = self.gateway.get_businesses(
            limit=DEFAULT_BUSINESSES_PAGE_LIMIT,
            offset=0,
        )
        return businesses