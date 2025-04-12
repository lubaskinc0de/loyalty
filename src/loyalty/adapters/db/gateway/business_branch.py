from dataclasses import dataclass
from uuid import UUID

from sqlalchemy.orm import Session

from loyalty.application.common.gateway.business_branch import BusinessBranchGateway
from loyalty.domain.entity.business_branch import BusinessBranch


@dataclass(slots=True, frozen=True)
class SABusinessBranchGateway(BusinessBranchGateway):
    session: Session

    def get_by_id(self, business_branch_id: UUID) -> BusinessBranch | None:
        res = self.session.get(BusinessBranch, business_branch_id)
        return res
