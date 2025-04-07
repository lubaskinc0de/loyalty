from abc import abstractmethod
from typing import Protocol

from loyalty.domain.entity.business import Business


class BusinessGateway(Protocol):
    @abstractmethod
    def insert(self, business: Business) -> None: ...
