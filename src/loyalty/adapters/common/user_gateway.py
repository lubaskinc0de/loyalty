from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from loyalty.adapters.auth.access_token import AccessToken
from loyalty.adapters.auth.user import WebUser
from loyalty.domain.entity.business import Business
from loyalty.domain.entity.client import Client


class WebUserGateway(Protocol):
    @abstractmethod
    def insert(self, user: WebUser) -> None: ...

    @abstractmethod
    def get_associated_account(self, user_id: UUID) -> Client | Business | None: ...

    @abstractmethod
    def get_by_username(self, username: str) -> WebUser | None: ...

    @abstractmethod
    def get_access_token(self, token: str) -> AccessToken | None: ...
