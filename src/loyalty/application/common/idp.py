from abc import abstractmethod
from typing import Protocol

from loyalty.domain.entity.business import Business
from loyalty.domain.entity.client import Client


class ClientIdProvider(Protocol):
    @abstractmethod
    def get_client(self) -> Client: ...


class BusinessIdProvider(Protocol):
    @abstractmethod
    def get_business(self) -> Business: ...
