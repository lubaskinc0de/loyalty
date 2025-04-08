from abc import abstractmethod
from typing import Protocol

from loyalty.domain.entity.business import Business
from loyalty.domain.entity.client import Client
from loyalty.domain.entity.user import Role, User


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
    def ensure_one_of(self, *roles: Role) -> None: ...


class UserIdProvider(Protocol):
    @abstractmethod
    def get_user(self) -> User: ...
