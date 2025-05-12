from collections.abc import Sequence
from dataclasses import dataclass
from uuid import UUID

from loyalty.application.common.gateway.membership import MembershipGateway
from loyalty.application.common.idp import ClientIdProvider
from loyalty.application.common.uow import UoW
from loyalty.application.exceptions.base import AccessDeniedError, InvalidPaginationQueryError, LimitIsTooHighError
from loyalty.application.exceptions.membership import MembershipDoesNotExistError
from loyalty.application.membership.dto import MembershipData, convert_membership_to_dto
from loyalty.application.shared_types import MAX_LIMIT

DEFAULT_MEMBERSHIPS_PAGE_LIMIT = 10


@dataclass(slots=True, frozen=True)
class ReadMembership:
    uow: UoW
    idp: ClientIdProvider
    gateway: MembershipGateway

    def execute(self, membership_id: UUID) -> MembershipData:
        client = self.idp.get_client()
        membership = self.gateway.get_by_id(membership_id)
        if membership is None:
            raise MembershipDoesNotExistError
        if not membership.can_read(client):
            raise AccessDeniedError

        return convert_membership_to_dto(membership)


@dataclass(slots=True, frozen=True)
class ReadMemberships:
    uow: UoW
    idp: ClientIdProvider
    gateway: MembershipGateway

    def execute(
        self,
        offset: int,
        limit: int = DEFAULT_MEMBERSHIPS_PAGE_LIMIT,
    ) -> Sequence[MembershipData]:
        client = self.idp.get_client()
        if limit > MAX_LIMIT:
            raise LimitIsTooHighError

        if limit < 0 or offset < 0:
            raise InvalidPaginationQueryError

        memberships = self.gateway.get_by_client_id(client.client_id, limit, offset)
        return memberships
