from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from loyalty.domain.entity.loyalty import Loyalty


class LoyaltyGateway(Protocol):
    @abstractmethod
    def get_by_id(self, loyalty_id: UUID) -> Loyalty | None: ...
