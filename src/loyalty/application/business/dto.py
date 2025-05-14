from collections.abc import Sequence
from dataclasses import dataclass

from loyalty.domain.entity.business import Business


@dataclass(slots=True)
class Businesses:
    businesses: Sequence[Business]
