from collections.abc import Sequence
from dataclasses import dataclass
from uuid import UUID

from adaptix.conversion import coercer

from loyalty.application.data_model.business_branch import BusinessBranchData, convert_branches_to_dto
from loyalty.domain.entity.business_branch import BusinessBranch


@dataclass(slots=True)
class BusinessBranches:
    business_id: UUID
    branches: Sequence[BusinessBranchData]


branches_coercer = coercer(
    Sequence[BusinessBranch],
    Sequence[BusinessBranchData],
    lambda x: convert_branches_to_dto(x),
)
