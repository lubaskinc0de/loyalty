from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class BusinessBranchId:
    branch_id: UUID


@dataclass(slots=True)
class LoyaltyId:
    loyalty_id: UUID


@dataclass(slots=True)
class MembershipId:
    membership_id: UUID
