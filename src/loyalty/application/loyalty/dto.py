from collections.abc import Sequence
from dataclasses import dataclass
from uuid import UUID

from loyalty.domain.entity.loyalty import Loyalty


@dataclass(slots=True)
class Loyalties:
    business_id: UUID | None
    loyalties: Sequence[Loyalty]
