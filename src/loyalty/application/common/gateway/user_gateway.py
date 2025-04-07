from abc import abstractmethod
from typing import Protocol

from loyalty.adapters.user import User


class UserGateway(Protocol):
    @abstractmethod
    def insert(self, user: User) -> None: ...
