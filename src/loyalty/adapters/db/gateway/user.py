from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from loyalty.adapters.auth.access_token import AccessToken
from loyalty.adapters.auth.user import WebUser
from loyalty.adapters.common.gateway import AccessTokenGateway, WebUserGateway
from loyalty.adapters.exceptions.user import WebUserAlreadyExistsError
from loyalty.application.common.gateway.user import UserGateway
from loyalty.domain.entity.user import User


@dataclass(slots=True, frozen=True)
class AuthGateway(UserGateway, AccessTokenGateway, WebUserGateway):
    session: Session

    def try_insert_unique(self, web_user: WebUser) -> None:
        try:
            self.session.add(web_user)
            self.session.flush((web_user,))
        except IntegrityError as e:
            match e.orig.diag.constraint_name:  # type: ignore
                case "ix_web_user_username":
                    raise WebUserAlreadyExistsError from e
                case _:
                    raise

    def get_by_username(self, username: str) -> WebUser | None:
        q = select(WebUser).filter_by(username=username)
        return self.session.execute(q).scalar_one_or_none()

    def get_by_id(self, user_id: UUID) -> User | None:
        q = select(User).filter_by(user_id=user_id)
        return self.session.execute(q).scalar_one_or_none()

    def get_access_token(self, token: str) -> AccessToken | None:
        q = select(AccessToken).filter_by(token=token)
        return self.session.execute(q).scalar_one_or_none()

    def delete_all_tokens(self, user_id: UUID) -> None:
        q = delete(AccessToken).filter_by(user_id=user_id)
        self.session.execute(q)
