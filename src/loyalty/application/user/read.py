from dataclasses import dataclass

from loyalty.application.common.idp import UserIdProvider
from loyalty.domain.entity.user import User


@dataclass(slots=True, frozen=True)
class ReadUser:
    idp: UserIdProvider

    def execute(self) -> User:
        return self.idp.get_user()
