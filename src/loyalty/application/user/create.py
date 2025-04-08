from dataclasses import dataclass
from uuid import uuid4

from loyalty.application.common.auth_provider import AuthProvider
from loyalty.application.common.uow import UoW
from loyalty.domain.entity.user import User


@dataclass(slots=True, frozen=True)
class CreateUser:
    uow: UoW
    auth: AuthProvider

    def execute(self) -> User:
        user = User(
            user_id=uuid4(),
        )
        self.uow.add(user)
        self.uow.flush((user,))

        self.auth.bind_to_auth(user)
        self.uow.commit()

        return user
