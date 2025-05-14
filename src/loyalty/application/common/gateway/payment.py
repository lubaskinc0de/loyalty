from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from loyalty.domain.entity.payment import Payment


class PaymentGateway(Protocol):
    @abstractmethod
    def get_by_id(self, payment_id: UUID) -> Payment | None: ...
