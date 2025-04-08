from dataclasses import dataclass

from loyalty.adapters.common.gateway import AccessTokenGateway
from loyalty.application.common.idp import UserIdProvider
from loyalty.application.common.uow import UoW


@dataclass(slots=True, frozen=True)
class Logout:
    idp: UserIdProvider
    token_gateway: AccessTokenGateway
    uow: UoW

    def execute(self) -> None:
        user = self.idp.get_user()
        self.token_gateway.delete_all_tokens(user.user_id)
        self.uow.commit()
