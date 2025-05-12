from collections.abc import Sequence
from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from loyalty.adapters.db import loyalty_membership_table, loyalty_table
from loyalty.application.common.gateway.membership import MembershipGateway
from loyalty.application.exceptions.membership import MembershipAlreadyExistError
from loyalty.application.membership.dto import MembershipData, convert_memberships_to_dto
from loyalty.domain.entity.membership import LoyaltyMembership


@dataclass(slots=True, frozen=True)
class SAMembershipGateway(MembershipGateway):
    session: Session

    def get_by_id(self, membership_id: UUID) -> LoyaltyMembership | None:
        q = select(LoyaltyMembership).filter_by(membership_id=membership_id)
        res = self.session.execute(q).scalar_one_or_none()
        return res

    def get_by_client_id(
        self,
        client_id: UUID,
        limit: int,
        offset: int,
        business_id: UUID | None = None,
    ) -> Sequence[MembershipData]:
        q = (
            select(LoyaltyMembership)
            .filter_by(client_id=client_id)
            .limit(limit)
            .offset(offset)
            .order_by(
                loyalty_membership_table.c.created_at,
            )
        )

        if business_id is not None:
            q = q.join(loyalty_table, loyalty_table.c.loyalty_id == loyalty_membership_table.c.loyalty_id).where(
                loyalty_table.c.business_id == business_id,
            )
        res = self.session.execute(q).scalars().all()
        data = convert_memberships_to_dto(res)
        return data  # type: ignore

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
