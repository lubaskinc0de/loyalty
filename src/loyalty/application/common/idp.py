from abc import abstractmethod
from typing import Protocol

from loyalty.domain.entity.business import Business
from loyalty.domain.entity.business_branch import BusinessBranch
from loyalty.domain.entity.client import Client
from loyalty.domain.entity.user import User


class ClientIdProvider(Protocol):
    @abstractmethod
    def get_client(self) -> Client: ...


class BusinessIdProvider(Protocol):
    @abstractmethod
    def get_business(self) -> Business: ...


class UserIdProvider(Protocol):
    @abstractmethod
    def get_user(self) -> User: ...


class BusinessBranchIdProvider(Protocol):
    @abstractmethod
    def get_business_branch(self) -> BusinessBranch: ...
