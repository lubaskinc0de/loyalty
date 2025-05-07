from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from loyalty.application.loyalty.dto import Loyalties
from loyalty.domain.entity.loyalty import Loyalty
from loyalty.domain.shared_types import Gender, LoyaltyTimeFrame


class LoyaltyGateway(Protocol):
    @abstractmethod
    def get_by_id(self, loyalty_id: UUID) -> Loyalty | None: ...

    @abstractmethod
    def get_loyalties(
        self,
        limit: int,
        offset: int,
        business_id: UUID | None,
        time_frame: LoyaltyTimeFrame,
        active: bool | None = None,
        client_age: int | None = None,
        client_gender: Gender | None = None,
    ) -> Loyalties: ...

    @abstractmethod
    def try_insert_unique(self, loyalty: Loyalty) -> None: ...
