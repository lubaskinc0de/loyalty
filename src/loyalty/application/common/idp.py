from abc import abstractmethod
from typing import Protocol
from uuid import UUID


class AuthProvider(Protocol):
    @abstractmethod
    def bind_client_auth(self, client_id: UUID) -> None: ...

    @abstractmethod
    def bind_business_auth(self, business_id: UUID) -> None: ...
