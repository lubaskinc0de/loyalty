from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from loyalty.application.common.gateway.bonus import BonusGateway
from loyalty.application.common.gateway.membership import MembershipGateway
from loyalty.application.common.idp import ClientIdProvider
from loyalty.application.exceptions.base import AccessDeniedError
from loyalty.application.exceptions.membership import MembershipDoesNotExistError


@dataclass(slots=True, frozen=True)
class BonusBalance:
    balance: Decimal


@dataclass(slots=True, frozen=True)
class ReadBonuses:
    gateway: BonusGateway
    membership_gateway: MembershipGateway
    idp: ClientIdProvider

    def execute(self, membership_id: UUID) -> BonusBalance:
        client = self.idp.get_client()
        membership = self.membership_gateway.get_by_id(membership_id)

        if membership is None:
            raise MembershipDoesNotExistError

        if not membership.is_owner_client(client):
            raise AccessDeniedError

        balance = self.gateway.get_bonus_balance(membership_id)
        return BonusBalance(balance)
