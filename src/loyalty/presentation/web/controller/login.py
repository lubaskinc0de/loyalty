from dataclasses import dataclass
from uuid import UUID

from loyalty.adapters.auth.access_token import AccessToken
from loyalty.adapters.auth.hasher import Hasher
from loyalty.adapters.auth.idp.token_processor import AccessTokenProcessor
from loyalty.adapters.auth.provider import WebUserCredentials
from loyalty.adapters.common.gateway import WebUserGateway
from loyalty.application.common.uow import UoW
from loyalty.application.exceptions.base import AccessDeniedError


@dataclass(slots=True, frozen=True)
class TokenResponse:
    user_id: UUID
    token: str


@dataclass(slots=True, frozen=True)
class WebLogin:
    web_user_gateway: WebUserGateway
    hasher: Hasher
    uow: UoW
    processor: AccessTokenProcessor

    def execute(self, form: WebUserCredentials) -> TokenResponse:
        web_user = self.web_user_gateway.get_by_username(form.username)
        if web_user is None:
            raise AccessDeniedError

        password_match = self.hasher.compare(form.password, web_user.hashed_password)
        if password_match is False:
            raise AccessDeniedError

        if not web_user.user.available_roles:
            self.uow.delete(web_user.user)
            self.uow.commit()
            raise AccessDeniedError

        token = AccessToken(
            user_id=web_user.user.user_id,
            token=self.processor.encode(user_id=web_user.user.user_id),
            user=web_user.user,
        )
        self.uow.add(token)
        self.uow.commit()

        return TokenResponse(user_id=token.user_id, token=token.token)
