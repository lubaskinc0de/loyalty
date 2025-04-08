from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from loyalty.adapters.auth.access_token import AccessToken
from loyalty.domain.entity.user import User


class WebUserGateway(Protocol):
    @abstractmethod
    def insert(self, user: User) -> None: ...

    @abstractmethod
    def get_by_id(self, user_id: UUID) -> User | None: ...

    @abstractmethod
    def get_by_username(self, username: str) -> User | None: ...

    @abstractmethod
    def get_access_token(self, token: str) -> AccessToken | None: ...

    @abstractmethod
    def delete_all_tokens(self, user_id: UUID) -> None: ...
