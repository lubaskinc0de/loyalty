from abc import abstractmethod
from typing import Protocol

from loyalty.domain.entity.business import Business
from loyalty.domain.entity.client import Client


class AuthProvider(Protocol):
    @abstractmethod
    def bind_client_to_auth(self, client: Client) -> None: ...

    @abstractmethod
    def bind_business_to_auth(self, business: Business) -> None: ...
