from dataclasses import dataclass
from uuid import UUID

from loyalty.application.common.gateway.membership import MembershipGateway
from loyalty.application.common.idp import ClientIdProvider
from loyalty.application.common.uow import UoW
from loyalty.application.exceptions.base import AccessDeniedError
from loyalty.application.exceptions.membership import MembershipDoesNotExistError


@dataclass(slots=True, frozen=True)
class DeleteMembership:
    uow: UoW
    idp: ClientIdProvider
    gateway: MembershipGateway

    def execute(self, membership_id: UUID) -> None:
        client = self.idp.get_client()
        membership = self.gateway.get_by_id(membership_id)

        if membership is None:
            raise MembershipDoesNotExistError

        if not membership.can_edit(client):
            raise AccessDeniedError

        self.uow.delete(membership)
        self.uow.commit()
