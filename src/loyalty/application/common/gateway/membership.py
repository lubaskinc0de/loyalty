from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from loyalty.domain.entity.membership import LoyaltyMembership


class MembershipGateway(Protocol):
    @abstractmethod
    def get_by_id(self, membership_id: UUID) -> LoyaltyMembership | None: ...

    @abstractmethod
    def try_insert_unique(self, membership: LoyaltyMembership) -> None:
        """Метод должен проверить, что членство в программе лояльности уникально,
        а если нет - выбросить MembershipAlreadyExistError.
        """
