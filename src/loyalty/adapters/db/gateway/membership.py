from collections.abc import Sequence
from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from loyalty.application.common.gateway.membership import MembershipGateway
from loyalty.application.exceptions.membership import MembershipAlreadyExistError
from loyalty.domain.entity.membership import LoyaltyMembership


@dataclass(slots=True, frozen=True)
class SAMembershipGateway(MembershipGateway):
    session: Session

    def get_by_id(self, membership_id: UUID) -> LoyaltyMembership | None:
        q = select(LoyaltyMembership).filter_by(membership_id=membership_id)
        res = self.session.execute(q).scalar_one_or_none()
        return res

    def get_by_client_id(self, client_id: UUID, limit: int, offset: int) -> Sequence[LoyaltyMembership]:
        q = select(LoyaltyMembership).filter_by(client_id=client_id).limit(limit).offset(offset)
        res = self.session.execute(q).scalars().all()
        return res

    def try_insert_unique(self, membership: LoyaltyMembership) -> None:
        try:
            self.session.add(membership)
            self.session.flush((membership,))
        except IntegrityError as e:
            match e.orig.diag.constraint_name:  # type: ignore
                case "uq_membership":
                    raise MembershipAlreadyExistError from e
                case _:
                    raise
