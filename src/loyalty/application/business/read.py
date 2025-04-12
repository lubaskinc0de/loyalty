from dataclasses import dataclass
from uuid import UUID

from loyalty.application.common.gateway.business import BusinessGateway
from loyalty.application.common.idp import UserIdProvider
from loyalty.application.exceptions.base import AccessDeniedError
from loyalty.application.exceptions.business import BusinessDoesNotExistsError
from loyalty.domain.entity.business import Business
from loyalty.domain.entity.user import Role


@dataclass(slots=True, frozen=True)
class ReadBusiness:
    idp: UserIdProvider
    gateway: BusinessGateway

    def execute(self, business_id: UUID) -> Business:
        user = self.idp.get_user()
        if not user.is_one_of(Role.CLIENT, Role.BUSINESS):
            raise AccessDeniedError
        if (business := self.gateway.get_by_id(business_id)) is None:
            raise BusinessDoesNotExistsError
        return business
