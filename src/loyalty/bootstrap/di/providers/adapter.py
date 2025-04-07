from argon2 import PasswordHasher
from dishka import AnyOf, Provider, Scope, from_context, provide
from sqlalchemy.orm import Session

from loyalty.adapters.config_loader import JWTConfig
from loyalty.adapters.db.provider import get_engine, get_session, get_sessionmaker
from loyalty.adapters.hasher import ArgonHasher, Hasher
from loyalty.adapters.idp.jwt_processor import AccessTokenProcessor
from loyalty.adapters.idp.token_parser import AccessTokenParser
from loyalty.adapters.idp.web import FlaskTokenParser, WebBusinessIdProvider, WebClientIdProvider
from loyalty.adapters.web_auth import AuthUserId, WebAuthProvider
from loyalty.application.common.auth_provider import AuthProvider
from loyalty.application.common.idp import BusinessIdProvider, ClientIdProvider
from loyalty.application.common.uow import UoW


class AdapterProvider(Provider):
    hasher = provide(ArgonHasher, provides=Hasher, scope=Scope.APP)
    auth_user_id = from_context(AuthUserId, scope=Scope.ACTION)
    token_parser = provide(FlaskTokenParser, provides=AccessTokenParser, scope=Scope.REQUEST)
    client_idp = provide(WebClientIdProvider, provides=ClientIdProvider, scope=Scope.REQUEST)
    business_idp = provide(WebBusinessIdProvider, provides=BusinessIdProvider, scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    def argon(self) -> PasswordHasher:
        return PasswordHasher()

    @provide(scope=Scope.ACTION)
    def simple_auth_provider(self, auth_user_id: AuthUserId, uow: UoW) -> AuthProvider:
        return WebAuthProvider(auth_user_id, uow)

    @provide(scope=Scope.APP)
    def token_processor(self, config: JWTConfig) -> AccessTokenProcessor:
        return AccessTokenProcessor(secret_key=config.secret_key)


def adapter_provider() -> AdapterProvider:
    provider = AdapterProvider()
    provider.provide(get_engine, scope=Scope.APP)
    provider.provide(get_sessionmaker, scope=Scope.APP)
    provider.provide(get_session, provides=AnyOf[Session, UoW], scope=Scope.REQUEST)

    return provider
