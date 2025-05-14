from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from adaptix.conversion import get_converter

from loyalty.application.business_branch.dto import branches_coercer
from loyalty.application.data_model.business_branch import BusinessBranchData
from loyalty.domain.entity.business import Business
from loyalty.domain.entity.loyalty import Loyalty
from loyalty.domain.shared_types import Gender


@dataclass(slots=True, frozen=True)
class LoyaltyData:
    loyalty_id: UUID
    name: str
    description: str
    starts_at: datetime
    ends_at: datetime
    money_per_bonus: Decimal
    min_age: int
    max_age: int
    business: Business
    money_for_bonus: Decimal
    is_active: bool
    gender: Gender | None
    business_branches: list[BusinessBranchData]
    created_at: datetime


@dataclass(slots=True, frozen=True)
class Loyalties:
    business_id: UUID | None
    loyalties: Sequence[LoyaltyData]


convert_loyalties_to_dto = get_converter(
    Sequence[Loyalty],
    Sequence[LoyaltyData],
    recipe=[branches_coercer],
)

convert_loyalty_to_dto = get_converter(
    Loyalty,
    LoyaltyData,
    recipe=[branches_coercer],
)
