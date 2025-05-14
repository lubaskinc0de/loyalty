from dataclasses import dataclass
from uuid import UUID

from loyalty.application.common.gateway.business import BusinessGateway
from loyalty.application.common.idp import UserIdProvider
from loyalty.application.exceptions.base import AccessDeniedError
from loyalty.application.exceptions.business import BusinessDoesNotExistError
from loyalty.domain.entity.business import Business


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

        if user.business and user.business.business_id != business_id:
            raise AccessDeniedError

        return business
