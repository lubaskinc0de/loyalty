from dataclasses import dataclass, field

from flask import Request
from jwt import PyJWTError

from loyalty.adapters.idp.access_token import AccessToken
from loyalty.adapters.idp.error import UnauthorizedError
from loyalty.adapters.idp.jwt_processor import AccessTokenProcessor
from loyalty.adapters.idp.token_parser import AccessTokenParser
from loyalty.application.common.gateway.business_gateway import BusinessGateway
from loyalty.application.common.gateway.client_gateway import ClientGateway
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
            return self.processor.decode(token)
        except PyJWTError as err:
            raise UnauthorizedError from err


@dataclass(slots=True)
class WebClientIdProvider(ClientIdProvider):
    token_parser: AccessTokenParser
    gateway: ClientGateway
    client: Client | None = field(init=False, repr=False, default=None)

    def get_client(self) -> Client:
        if self.client is not None:  # cache
            return self.client

        token = self.token_parser.authorize_by_token()
        if token.role != "client":
            raise AccessDeniedError
        client = self.gateway.get_by_id(token.entity_id)
        if client is None:
            raise UnauthorizedError

        self.client = client
        return client


@dataclass(slots=True)
class WebBusinessIdProvider(BusinessIdProvider):
    token_parser: AccessTokenParser
    gateway: BusinessGateway
    business: Business | None = field(init=False, repr=False, default=None)

    def get_business(self) -> Business:
        if self.business is not None:  # cache
            return self.business

        token = self.token_parser.authorize_by_token()
        if token.role != "business":
            raise AccessDeniedError
        business = self.gateway.get_by_id(token.entity_id)
        if business is None:
            raise UnauthorizedError

        self.business = business
        return business
