from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from loyalty.adapters.db.table.business_branch import business_branch_table
from loyalty.application.business_branch.dto import BusinessBranchesDTO
from loyalty.application.common.gateway.business import BusinessGateway
from loyalty.application.exceptions.business import BusinessAlreadyExistsError
from loyalty.domain.entity.business import Business
from loyalty.domain.entity.business_branch import BusinessBranch


@dataclass(slots=True, frozen=True)
class SABusinessGateway(BusinessGateway):
    session: Session

    def try_insert_unique(self, business: Business) -> None:
        try:
            self.session.add(business)
            self.session.flush((business,))
        except IntegrityError as e:
            match e.orig.diag.constraint_name:  # type: ignore
                case "business_name_key":
                    raise BusinessAlreadyExistsError from e
                case _:
                    raise

    def get_by_id(self, business_id: UUID) -> Business | None:
        q = select(Business).filter_by(business_id=business_id)
        res = self.session.execute(q).scalar_one_or_none()
        return res

    def get_branches(self, limit: int, offset: int, business_id: UUID) -> BusinessBranchesDTO:
        q = (
            select(BusinessBranch)
            .where(business_branch_table.c.business_id == business_id)
            .limit(limit + 1)
            .offset(offset)
            .order_by(business_branch_table.c.created_at)
        )

        res = self.session.execute(q)
        business_branches = [row[0] for row in res.all()]

        has_next = False

        if len(business_branches) > limit:
            has_next = True

            business_branches.pop()

        return BusinessBranchesDTO(
            business_id=business_id,
            business_branches=business_branches,
            has_next=has_next,
        )
