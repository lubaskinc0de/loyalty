from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from adaptix.conversion import coercer, get_converter

from loyalty.application.loyalty.dto import LoyaltyData, convert_loyalty_to_dto
from loyalty.domain.entity.client import Client
from loyalty.domain.entity.loyalty import Loyalty
from loyalty.domain.entity.membership import LoyaltyMembership


@dataclass(slots=True, frozen=True)
class MembershipData:
    loyalty: LoyaltyData
    client: Client
    membership_id: UUID
    created_at: datetime


loyalty_coercer = coercer(
    Loyalty,
    LoyaltyData,
    lambda x: convert_loyalty_to_dto(x),
)
convert_membership_to_dto = get_converter(LoyaltyMembership, MembershipData, recipe=[loyalty_coercer])
convert_memberships_to_dto = get_converter(
    Sequence[LoyaltyMembership],
    Sequence[MembershipData],
    recipe=[loyalty_coercer],
)
