from dataclasses import dataclass
from loyalty.domain.entity.business_branch import BusinessBranch


@dataclass(slots=True)
class BusinessBranchList:
    branches: list[BusinessBranch]
