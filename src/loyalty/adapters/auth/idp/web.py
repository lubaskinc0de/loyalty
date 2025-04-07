from dataclasses import dataclass, field

from flask import Request
from jwt import PyJWTError

from loyalty.adapters.auth.access_token import AccessToken
from loyalty.adapters.auth.idp.error import UnauthorizedError
from loyalty.adapters.auth.idp.token_parser import AccessTokenParser
from loyalty.adapters.auth.idp.token_processor import AccessTokenProcessor
from loyalty.adapters.common.user_gateway import WebUserGateway
from loyalty.application.common.idp import BusinessIdProvider, ClientIdProvider, Role, RoleProvider
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

        try:
            self.processor.verify(token)
        except PyJWTError as err:
            raise UnauthorizedError from err

        db_token = self.gateway.get_access_token(token)
        if db_token is None:
            raise UnauthorizedError

        return db_token


@dataclass(slots=True)
class WebIdProvider(ClientIdProvider, BusinessIdProvider, RoleProvider):
    token_parser: AccessTokenParser
    gateway: WebUserGateway
    client: Client | None = field(init=False, repr=False, default=None)
    business: Business | None = field(init=False, repr=False, default=None)
    token: AccessToken | None = field(init=False, repr=False, default=None)

    def available_roles(self) -> list[Role]:
        token = self.token_parser.authorize_by_token() if self.token is None else self.token
        return token.user.available_roles

    def ensure_one_of(self, roles: list[Role]) -> None:
        available = self.available_roles()
        matches = [x for x in roles if x in available]

        if not matches:
            raise AccessDeniedError

    def get_business(self) -> Business:
        if self.business is not None:
            return self.business

        token = self.token_parser.authorize_by_token() if self.token is None else self.token

        if Role.BUSINESS not in token.user.available_roles or token.user.business is None:
            raise AccessDeniedError

        self.business = token.user.business
        self.token = token
        return self.business

    def get_client(self) -> Client:
        if self.client is not None:
            return self.client

        token = self.token_parser.authorize_by_token() if self.token is None else self.token
        if Role.CLIENT not in token.user.available_roles or token.user.client is None:
            raise AccessDeniedError

        self.client = token.user.client
        self.token = token
        return self.client
