from abc import abstractmethod
from typing import Protocol

from loyalty.adapters.idp.access_token import AccessToken


class AccessTokenParser(Protocol):
    @abstractmethod
    def authorize_by_token(self) -> AccessToken: ...
