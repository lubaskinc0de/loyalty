from dataclasses import dataclass
from uuid import UUID

from loyalty.domain.entity.business_branch import BusinessBranch
from loyalty.domain.entity.loyalty import Loyalty


@dataclass(slots=True)
class BusinessBranchList:
    branches: list[BusinessBranch]


@dataclass(slots=True)
class BusinessBranchId:
    branch_id: UUID


@dataclass(slots=True)
class LoyaltyId:
    loyalty_id: UUID


@dataclass(slots=True)
class MembershipId:
    membership_id: UUID


@dataclass(slots=True)
class LoyaltyList:
    loyalties: list[Loyalty]
