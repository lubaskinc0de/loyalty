from dataclasses import dataclass
from typing import NewType
from uuid import UUID

from loyalty.adapters.db.table.user import ClientUser
from loyalty.application.common.idp import IdProvider
from loyalty.application.common.uow import UoW

AuthUserId = NewType("AuthUserId", UUID)


@dataclass(slots=True, frozen=True)
class UserIdProvider(IdProvider):
    user_id: AuthUserId
    uow: UoW

    def bind_client_auth(self, client_id: UUID) -> None:
        client_user = ClientUser(client_id=client_id, user_id=self.user_id)
        self.uow.add(client_user)
