from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol
from uuid import UUID

from loyalty.application.business.dto import BusinessPaymentsStats
from loyalty.domain.entity.business import Business


class BusinessGateway(Protocol):
    @abstractmethod
    def try_insert_unique(self, business: Business) -> None:
        """Метод должен проверить, что у бизнеса уникальное название,
        а если нет - выбросить BusinessAlreadyExistsError.
        """

    @abstractmethod
    def get_by_id(self, business_id: UUID) -> Business | None: ...

    @abstractmethod
    def get_businesses(self, limit: int, offset: int) -> Sequence[Business]: ...

    @abstractmethod
    def get_business_payments_stat(self, business_id: UUID) -> BusinessPaymentsStats: ...

    @abstractmethod
    def get_business_loyalties_count(self, business_id: UUID) -> int: ...

    @abstractmethod
    def get_business_memberships_count(self, business_id: UUID) -> int: ...
