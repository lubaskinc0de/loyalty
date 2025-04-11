from dataclasses import dataclass
from uuid import UUID

from loyalty.domain.entity.business_branch import BusinessBranch


@dataclass(slots=True)
class BusinessBranchesDTO:
    business_id: UUID
    business_branches: list[BusinessBranch]
    has_next: bool
