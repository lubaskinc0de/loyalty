from dataclasses import dataclass
from typing import NewType
from uuid import UUID

from loyalty.adapters.db.table.user import BusinessUser, ClientUser
from loyalty.application.common.idp import AuthProvider
from loyalty.application.common.uow import UoW

AuthUserId = NewType("AuthUserId", UUID)


@dataclass(slots=True, frozen=True)
class SimpleAuthProvider(AuthProvider):
    user_id: AuthUserId
    uow: UoW

    def bind_client_auth(self, client_id: UUID) -> None:
        client_user = ClientUser(client_id=client_id, user_id=self.user_id)
        self.uow.flush((client_user, ))
        self.uow.add(client_user)

    def bind_business_auth(self, business_id: UUID) -> None:
        business_user = BusinessUser(business_id=business_id, user_id=self.user_id)
        self.uow.flush((business_user, ))
        self.uow.add(business_user)
