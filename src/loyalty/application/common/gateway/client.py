from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from loyalty.domain.entity.client import Client


class ClientGateway(Protocol):
    @abstractmethod
    def get_by_id(self, client_id: UUID) -> Client | None: ...
