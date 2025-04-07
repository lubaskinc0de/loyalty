from dataclasses import dataclass
from uuid import UUID

from loyalty.adapters.auth.access_token import AccessToken
from loyalty.adapters.auth.hasher import Hasher
from loyalty.adapters.auth.idp.token_processor import AccessTokenProcessor
from loyalty.adapters.common.user_gateway import WebUserGateway
from loyalty.application.common.uow import UoW
from loyalty.application.exceptions.base import AccessDeniedError
from loyalty.presentation.web.controller.user import WebUserCredentials


@dataclass(slots=True, frozen=True)
class TokenResponse:
    user_id: UUID
    token: str


@dataclass(slots=True, frozen=True)
class WebLogin:
    user_gateway: WebUserGateway
    hasher: Hasher
    uow: UoW
    processor: AccessTokenProcessor

    def execute(self, form: WebUserCredentials) -> TokenResponse:
        user = self.user_gateway.get_by_username(form.username)
        if user is None:
            raise AccessDeniedError

        password_match = self.hasher.compare(form.password, user.hashed_password)
        if password_match is False:
            raise AccessDeniedError

        if not user.available_roles:
            self.uow.delete(user)
            self.uow.commit()
            raise AccessDeniedError

        token = AccessToken(user_id=user.user_id, token=self.processor.encode(user_id=user.user_id), user=user)
        self.uow.add(token)
        self.uow.commit()

        return TokenResponse(user_id=token.user_id, token=token.token)
