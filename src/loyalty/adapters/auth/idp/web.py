import logging
from dataclasses import dataclass, field

from flask import Request
from jwt import PyJWTError

from loyalty.adapters.auth.access_token import AccessToken
from loyalty.adapters.auth.idp.error import UnauthorizedError
from loyalty.adapters.auth.idp.token_parser import AccessTokenParser
from loyalty.adapters.auth.idp.token_processor import AccessTokenProcessor
from loyalty.adapters.common.gateway import AccessTokenGateway
from loyalty.application.common.gateway.user import UserGateway
from loyalty.application.common.idp import BusinessIdProvider, ClientIdProvider, RoleProvider, UserIdProvider
from loyalty.application.exceptions.base import AccessDeniedError
from loyalty.domain.entity.business import Business
from loyalty.domain.entity.client import Client
from loyalty.domain.entity.user import Role, User

TOKEN_TYPE = "Bearer"  # noqa: S105
BEARER_SECTIONS = 2
AUTH_HEADER = "Authorization"


@dataclass(slots=True, frozen=True)
class FlaskTokenParser(AccessTokenParser):
    request: Request
    processor: AccessTokenProcessor
    gateway: AccessTokenGateway

    def authorize_by_token(self) -> AccessToken:
        authorization_header = self.request.headers.get(AUTH_HEADER)

        if authorization_header is None:
            logging.info("Unauthorized due to auth header")
            raise UnauthorizedError

        sections = authorization_header.split(" ")
        if len(sections) != BEARER_SECTIONS:
            logging.info("Unauthorized due to bearer sections")
            raise UnauthorizedError

        token_type, token = sections

        if token_type != TOKEN_TYPE:
            logging.info("Unauthorized due to token type")
            raise UnauthorizedError

        try:
            self.processor.verify(token)
        except PyJWTError as err:
            logging.exception("JWT verify failed")
            raise UnauthorizedError from err

        db_token = self.gateway.get_access_token(token)
        if db_token is None:
            logging.info("Unauthorized due to db token")
            raise UnauthorizedError

        return db_token


@dataclass(slots=True)
class WebIdProvider(ClientIdProvider, BusinessIdProvider, RoleProvider, UserIdProvider):
    token_parser: AccessTokenParser
    gateway: UserGateway
    client: Client | None = field(init=False, repr=False, default=None)
    business: Business | None = field(init=False, repr=False, default=None)
    user: User | None = field(init=False, repr=False, default=None)

    def get_user(self) -> User:
        if self.user is not None:
            return self.user
        token = self.token_parser.authorize_by_token()
        self.user = token.user
        return self.user

    def available_roles(self) -> list[Role]:
        return self.get_user().available_roles

    def ensure_one_of(self, *roles: Role) -> None:
        available = self.available_roles()
        matches = [x for x in roles if x in available]

        if not matches:
            raise AccessDeniedError

    def get_business(self) -> Business:
        if self.business is not None:
            return self.business

        user = self.get_user()
        self.ensure_one_of(Role.BUSINESS)

        if user.business is None:
            raise AccessDeniedError

        self.business = user.business
        return self.business

    def get_client(self) -> Client:
        if self.client is not None:
            return self.client

        user = self.get_user()
        self.ensure_one_of(Role.CLIENT)

        if user.client is None:
            raise AccessDeniedError

        self.client = user.client
        return self.client
