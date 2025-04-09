from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from loyalty.adapters.auth.access_token import AccessToken
from loyalty.adapters.auth.user import WebUser


class WebUserGateway(Protocol):
    @abstractmethod
    def get_by_username(self, username: str) -> WebUser | None: ...

    @abstractmethod
    def try_insert_unique(self, web_user: WebUser) -> None:
        """Метод должен проверить что у WebUser
        уникальный username - иначе выбросить ошибку WebUserAlreadyExistsError.
        """


class AccessTokenGateway(Protocol):
    @abstractmethod
    def get_access_token(self, token: str) -> AccessToken | None: ...

    @abstractmethod
    def delete_all_tokens(self, user_id: UUID) -> None: ...
