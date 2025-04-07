from dataclasses import dataclass

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from loyalty.application.common.gateway.user_gateway import UserGateway
from loyalty.application.exceptions.user import UserAlreadyExistsError
from loyalty.adapters.user import User


@dataclass(slots=True, frozen=True)
class SAUserGateway(UserGateway):
    session: Session

    def insert(self, user: User) -> None:
        try:
            self.session.add(user)
            self.session.flush((user,))
        except IntegrityError as e:
            match e.orig.diag.constraint_name:  # type: ignore
                case "ix_users_username":
                    raise UserAlreadyExistsError from e
                case _:
                    raise
