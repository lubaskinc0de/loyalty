from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from loyalty.application.common.gateway.client import ClientGateway
from loyalty.domain.entity.client import Client


@dataclass(slots=True, frozen=True)
class SAClientGateway(ClientGateway):
    session: Session

    def get_by_id(self, client_id: UUID) -> Client | None:
        q = select(Client).filter_by(client_id=client_id)
        res = self.session.execute(q).scalar_one_or_none()
        return res
