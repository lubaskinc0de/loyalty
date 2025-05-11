from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol
from uuid import UUID

from loyalty.application.membership.dto import MembershipData
from loyalty.domain.entity.membership import LoyaltyMembership


class MembershipGateway(Protocol):
    @abstractmethod
    def get_by_id(self, membership_id: UUID) -> LoyaltyMembership | None: ...

    @abstractmethod
    def get_by_client_id(self, client_id: UUID, limit: int, offset: int) -> Sequence[MembershipData]: ...

    @abstractmethod
    def try_insert_unique(self, membership: LoyaltyMembership) -> None:
        """Метод должен проверить, что членство в программе лояльности уникально,
        а если нет - выбросить MembershipAlreadyExistError.
        """
