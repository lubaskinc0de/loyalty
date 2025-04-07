from dataclasses import dataclass
from typing import NewType
from uuid import UUID

from loyalty.adapters.db.table.user import BusinessUser, ClientUser
from loyalty.application.common.auth_provider import AuthProvider
from loyalty.application.common.uow import UoW
from loyalty.domain.entity.business import Business
from loyalty.domain.entity.client import Client

AuthUserId = NewType("AuthUserId", UUID)


@dataclass(slots=True, frozen=True)
class WebAuthProvider(AuthProvider):
    user_id: AuthUserId
    uow: UoW

    def bind_client_to_auth(self, client: Client) -> None:
        client_user = ClientUser(client_id=client.client_id, user_id=self.user_id, client=client)
        self.uow.flush((client_user,))
        self.uow.add(client_user)

    def bind_business_to_auth(self, business: Business) -> None:
        business_user = BusinessUser(business_id=business.business_id, user_id=self.user_id, business=business)
        self.uow.flush((business_user,))
        self.uow.add(business_user)
