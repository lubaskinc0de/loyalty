import logging
from dataclasses import dataclass
from uuid import UUID, uuid4

from pydantic import BaseModel

from loyalty.application.common.gateway.loyalty import LoyaltyGateway
from loyalty.application.common.gateway.membership import MembershipGateway
from loyalty.application.common.idp import ClientIdProvider
from loyalty.application.common.uow import UoW
from loyalty.application.exceptions.base import AccessDeniedError
from loyalty.application.exceptions.loyalty import LoyaltyDoesNotExistError
from loyalty.domain.entity.membership import LoyaltyMembership


class MembershipForm(BaseModel):
    loyalty_id: UUID


@dataclass(slots=True, frozen=True)
class CreateMembership:
    uow: UoW
    idp: ClientIdProvider
    loyalty_gateway: LoyaltyGateway
    membership_gateway: MembershipGateway

    def execute(self, form: MembershipForm) -> UUID:
        client = self.idp.get_client()
        loyalty = self.loyalty_gateway.get_by_id(form.loyalty_id)

        if loyalty is None:
            raise LoyaltyDoesNotExistError

        if not loyalty.match_targeting(client):
            logging.info("Restricted membership due to targeting")
            raise AccessDeniedError

        membership_id = uuid4()
        membership = LoyaltyMembership(
            membership_id=membership_id,
            loyalty=loyalty,
            client=client,
        )
        self.membership_gateway.try_insert_unique(membership)
        self.uow.commit()

        return membership_id
