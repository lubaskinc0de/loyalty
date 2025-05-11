from collections.abc import Sequence
from dataclasses import dataclass
from uuid import UUID

from loyalty.application.data_model.business_branch import BusinessBranchData


@dataclass(slots=True)
class BusinessBranches:
    business_id: UUID
    branches: Sequence[BusinessBranchData]
