from abc import abstractmethod
from typing import Protocol

from loyalty.domain.entity.user import User


class UserGateway(Protocol):
    @abstractmethod
    def insert(self, user: User) -> None:
        ...
