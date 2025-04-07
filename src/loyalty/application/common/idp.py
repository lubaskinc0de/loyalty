from abc import abstractmethod
from enum import Enum
from typing import Protocol

from loyalty.domain.entity.business import Business
from loyalty.domain.entity.client import Client


class Role(Enum):
    CLIENT = "client"
    BUSINESS = "business"


class ClientIdProvider(Protocol):
    @abstractmethod
    def get_client(self) -> Client: ...


class BusinessIdProvider(Protocol):
    @abstractmethod
    def get_business(self) -> Business: ...


class RoleProvider(Protocol):
    @abstractmethod
    def available_roles(self) -> list[Role]: ...

    @abstractmethod
    def ensure_one_of(self, roles: list[Role]) -> None: ...
