from dataclasses import dataclass
from uuid import UUID

from loyalty.domain.entity.business_branch import BusinessBranch


@dataclass(slots=True)
class BusinessBranches:
    business_id: UUID
    business_branches: list[BusinessBranch]
