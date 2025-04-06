from dataclasses import dataclass
from sqlite3 import IntegrityError

from sqlalchemy.orm import Session

from loyalty.application.common.gateway.user_gateway import UserGateway
from loyalty.application.exceptions.user import UserAlreadyExistsError
from loyalty.domain.entity.user import User


@dataclass(slots=True, frozen=True)
class SAUserGateway(UserGateway):
    session: Session

    def insert(self, user: User) -> None:
        try:
            self.session.add(user)
            self.session.flush((user,))
        except IntegrityError as e:
            match e.__cause__.__cause__.constraint_name:  # type: ignore
                case "uq_users_username":
                    raise UserAlreadyExistsError from e
                case _:
                    raise
