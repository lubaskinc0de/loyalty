from dataclasses import dataclass, field

from flask import Request
from jwt import PyJWTError

from loyalty.adapters.auth.access_token import AccessToken
from loyalty.adapters.auth.idp.error import UnauthorizedError
from loyalty.adapters.auth.idp.token_parser import AccessTokenParser
from loyalty.adapters.auth.idp.token_processor import AccessTokenProcessor
from loyalty.adapters.common.user_gateway import WebUserGateway
from loyalty.application.common.idp import BusinessIdProvider, ClientIdProvider
from loyalty.application.exceptions.base import AccessDeniedError
from loyalty.domain.entity.business import Business
from loyalty.domain.entity.client import Client

TOKEN_TYPE = "Bearer"  # noqa: S105
BEARER_SECTIONS = 2
AUTH_HEADER = "Authorization"


@dataclass(slots=True, frozen=True)
class FlaskTokenParser(AccessTokenParser):
    request: Request
    processor: AccessTokenProcessor
    gateway: WebUserGateway

    def authorize_by_token(self) -> AccessToken:
        authorization_header = self.request.headers.get(AUTH_HEADER)

        if authorization_header is None:
            raise UnauthorizedError

        sections = authorization_header.split(" ")
        if len(sections) != BEARER_SECTIONS:
            raise UnauthorizedError

        token_type, token = sections

        if token_type != TOKEN_TYPE:
            raise UnauthorizedError

        token_obj = None
        try:
            token_obj = self.processor.decode(token)
        except PyJWTError as err:
            raise UnauthorizedError from err

        db_token = self.gateway.get_access_token(token_obj.token)
        if db_token is None:
            raise UnauthorizedError

        if db_token.user_id != token_obj.user_id:
            raise UnauthorizedError

        return db_token


@dataclass(slots=True)
class WebClientIdProvider(ClientIdProvider):
    token_parser: AccessTokenParser
    gateway: WebUserGateway
    client: Client | None = field(init=False, repr=False, default=None)

    def get_client(self) -> Client:
        if self.client is not None:  # cache
            return self.client

        token = self.token_parser.authorize_by_token()
        account = self.gateway.get_associated_account(token.user_id)

        if account is None:
            raise UnauthorizedError

        if not isinstance(account, Client):
            raise AccessDeniedError

        self.client = account
        return account


@dataclass(slots=True)
class WebBusinessIdProvider(BusinessIdProvider):
    token_parser: AccessTokenParser
    gateway: WebUserGateway
    business: Business | None = field(init=False, repr=False, default=None)

    def get_business(self) -> Business:
        if self.business is not None:  # cache
            return self.business

        token = self.token_parser.authorize_by_token()
        account = self.gateway.get_associated_account(token.user_id)

        if account is None:
            raise UnauthorizedError

        if not isinstance(account, Business):
            raise AccessDeniedError

        self.business = account
        return account
