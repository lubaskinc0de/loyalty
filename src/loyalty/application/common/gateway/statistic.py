from abc import abstractmethod
from dataclasses import dataclass
from decimal import Decimal

from sqlalchemy.orm import Session


@dataclass(slots=True, frozen=True)
class StatisticsGateway:
    session: Session

    @abstractmethod
    def get_total_payments(self) -> Decimal: ...

    @abstractmethod
    def get_total_clients(self) -> int: ...

    @abstractmethod
    def get_total_businesses(self) -> int: ...
