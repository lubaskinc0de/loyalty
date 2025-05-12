from abc import abstractmethod
from decimal import Decimal
from typing import Protocol
from uuid import UUID


class BonusGateway(Protocol):
    @abstractmethod
    def calc_bonus_balance(self, membership_id: UUID) -> Decimal: ...
