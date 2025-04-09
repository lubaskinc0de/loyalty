from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from loyalty.domain.entity.business import Business


class BusinessGateway(Protocol):
    @abstractmethod
    def try_insert_unique(self, business: Business) -> None:
        """Метод должен проверить, что у бизнеса уникальное название,
        а если нет - выбросить BusinessAlreadyExistsError.
        """

    @abstractmethod
    def get_by_id(self, business_id: UUID) -> Business | None: ...
