from collections.abc import Sequence
from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from loyalty.adapters.db.table.business_branch import business_branch_table
from loyalty.application.business_branch.dto import BusinessBranches
from loyalty.application.common.gateway.business_branch import BusinessBranchGateway
from loyalty.domain.entity.business_branch import BusinessBranch


@dataclass(slots=True, frozen=True)
class SABusinessBranchGateway(BusinessBranchGateway):
    session: Session

    def get_by_id(self, business_branch_id: UUID) -> BusinessBranch | None:
        res = self.session.get(BusinessBranch, business_branch_id)
        return res

    def get_business_branches(self, limit: int, offset: int, business_id: UUID) -> BusinessBranches:
        q = (
            select(BusinessBranch)
            .where(business_branch_table.c.business_id == business_id)
            .limit(limit + 1)
            .offset(offset)
            .order_by(business_branch_table.c.created_at)
        )

        res = self.session.execute(q)
        return BusinessBranches(
            business_id=business_id,
            branches=res.scalars().all(),
        )

    def get_business_branches_by_id_list(self, business_branch_id_list: list[UUID]) -> Sequence[BusinessBranch]:
        return self.session.scalars(
            select(BusinessBranch).where(business_branch_table.c.business_branch_id.in_(business_branch_id_list)),
        ).all()
