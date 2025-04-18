from argon2 import PasswordHasher
from dishka import AnyOf, Provider, Scope, from_context, provide
from sqlalchemy.orm import Session

from loyalty.adapters.auth.hasher import ArgonHasher, Hasher
from loyalty.adapters.auth.idp.token_parser import AccessTokenParser
from loyalty.adapters.auth.idp.token_processor import AccessTokenProcessor
from loyalty.adapters.auth.idp.web import FlaskTokenParser, WebIdProvider
from loyalty.adapters.auth.provider import WebAuthProvider, WebUserCredentials
from loyalty.adapters.common.gateway import WebUserGateway
from loyalty.adapters.config_loader import JWTConfig
from loyalty.adapters.db.provider import get_engine, get_session, get_sessionmaker
from loyalty.application.common.auth_provider import AuthProvider
from loyalty.application.common.idp import BusinessIdProvider, ClientIdProvider, UserIdProvider
from loyalty.application.common.uow import UoW


class AdapterProvider(Provider):
    hasher = provide(ArgonHasher, provides=Hasher, scope=Scope.APP)
    form = from_context(WebUserCredentials, scope=Scope.ACTION)
    token_parser = provide(FlaskTokenParser, provides=AccessTokenParser, scope=Scope.REQUEST)
    idp = provide(
        WebIdProvider,
        provides=AnyOf[ClientIdProvider, BusinessIdProvider, UserIdProvider],
        scope=Scope.REQUEST,
    )

    @provide(scope=Scope.APP)
    def argon(self) -> PasswordHasher:
        return PasswordHasher()

    @provide(scope=Scope.ACTION)
    def web_auth_provider(self, form: WebUserCredentials, gateway: WebUserGateway, hasher: Hasher) -> AuthProvider:
        return WebAuthProvider(hasher, gateway, form)

    @provide(scope=Scope.APP)
    def token_processor(self, config: JWTConfig) -> AccessTokenProcessor:
        return AccessTokenProcessor(secret_key=config.secret_key)


def adapter_provider() -> AdapterProvider:
    provider = AdapterProvider()
    provider.provide(get_engine, scope=Scope.APP)
    provider.provide(get_sessionmaker, scope=Scope.APP)
    provider.provide(get_session, provides=AnyOf[Session, UoW], scope=Scope.REQUEST)

    return provider
