from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from loyalty.domain.entity.user import User


class UserGateway(Protocol):
    @abstractmethod
    def get_by_id(self, user_id: UUID) -> User | None: ...
