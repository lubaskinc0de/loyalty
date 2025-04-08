from abc import abstractmethod
from typing import Protocol

from loyalty.domain.entity.user import User


class AuthProvider(Protocol):
    @abstractmethod
    def bind_to_auth(self, user: User) -> None: ...
