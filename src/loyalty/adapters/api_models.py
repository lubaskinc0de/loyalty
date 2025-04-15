from dataclasses import dataclass
from uuid import UUID

from loyalty.domain.entity.business_branch import BusinessBranch


@dataclass(slots=True)
class BusinessBranchList:
    branches: list[BusinessBranch]


@dataclass(slots=True)
class BusinessBranchId:
    branch_id: UUID
