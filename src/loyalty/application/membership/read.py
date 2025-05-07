from dataclasses import dataclass

from loyalty.application.common.gateway.membership import MembershipGateway
from loyalty.application.common.idp import ClientIdProvider
from loyalty.application.common.uow import UoW
from loyalty.application.exceptions.membership import MembershipDoesNotExistError
from loyalty.domain.entity.membership import LoyaltyMembership


@dataclass(slots=True, frozen=True)
class ReadMembership:
    uow: UoW
    idp: ClientIdProvider
    gateway: MembershipGateway

    def execute(self) -> LoyaltyMembership:
        client = self.idp.get_client()
        membership = self.gateway.get_by_client_id(client.client_id)
        if membership is None:
            raise MembershipDoesNotExistError
        return membership
