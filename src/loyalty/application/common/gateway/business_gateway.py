from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from loyalty.domain.entity.business import Business


class BusinessGateway(Protocol):
    @abstractmethod
    def insert(self, business: Business) -> None: ...

    @abstractmethod
    def get_by_id(self, business_id: UUID) -> Business | None: ...
