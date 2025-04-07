from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from loyalty.adapters.common.user_gateway import WebUserGateway
from loyalty.adapters.db.table.user import BusinessUser, ClientUser
from loyalty.adapters.user import WebUser
from loyalty.application.exceptions.user import UserAlreadyExistsError
from loyalty.domain.entity.business import Business
from loyalty.domain.entity.client import Client


@dataclass(slots=True, frozen=True)
class SAUserGateway(WebUserGateway):
    session: Session

    def insert(self, user: WebUser) -> None:
        try:
            self.session.add(user)
            self.session.flush((user,))
        except IntegrityError as e:
            match e.orig.diag.constraint_name:  # type: ignore
                case "ix_users_username":
                    raise UserAlreadyExistsError from e
                case _:
                    raise

    def get_associated_account(self, user_id: UUID) -> Client | Business | None:
        q_client = select(ClientUser).filter_by(user_id=user_id)
        res_client = self.session.execute(q_client).scalar_one_or_none()

        if res_client is not None:
            return res_client.client

        q_business = select(BusinessUser).filter_by(user_id=user_id)
        res_business = self.session.execute(q_business).scalar_one_or_none()

        if res_business is not None:
            return res_business.business

        return None

    def get_by_username(self, username: str) -> WebUser | None:
        q = select(WebUser).filter_by(username=username)
        return self.session.execute(q).scalar_one_or_none()
