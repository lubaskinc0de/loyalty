from abc import abstractmethod
from typing import Protocol
from uuid import UUID


class IdProvider(Protocol):
    @abstractmethod
    def bind_client_auth(self, client_id: UUID) -> None:
        ...
