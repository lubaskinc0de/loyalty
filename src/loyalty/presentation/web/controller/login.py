from dataclasses import dataclass

from loyalty.adapters.common.user_gateway import WebUserGateway
from loyalty.adapters.hasher import Hasher
from loyalty.adapters.idp.access_token import AccessToken
from loyalty.adapters.idp.jwt_processor import AccessTokenProcessor
from loyalty.application.common.uow import UoW
from loyalty.application.exceptions.base import AccessDeniedError
from loyalty.domain.entity.client import Client
from loyalty.presentation.web.controller.user import WebUserCredentials


@dataclass(slots=True, frozen=True)
class TokenResponse:
    token_info: AccessToken
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

        associated_account = self.user_gateway.get_associated_account(user_id=user.user_id)
        if associated_account is None:
            self.uow.delete(user)
            self.uow.commit()
            raise AccessDeniedError

        if isinstance(associated_account, Client):
            token = AccessToken(role="client", entity_id=associated_account.client_id)
        else:
            token = AccessToken(role="business", entity_id=associated_account.business_id)

        return TokenResponse(token_info=token, token=self.processor.encode(token))
