from argon2 import PasswordHasher
from dishka import AnyOf, Provider, Scope, from_context, provide
from sqlalchemy.orm import Session

from loyalty.adapters.db.provider import get_engine, get_session, get_sessionmaker
from loyalty.adapters.hasher import ArgonHasher, Hasher
from loyalty.adapters.idp import AuthUserId, UserIdProvider
from loyalty.application.common.idp import IdProvider
from loyalty.application.common.uow import UoW


class AdapterProvider(Provider):
    hasher = provide(ArgonHasher, provides=Hasher, scope=Scope.APP)
    auth_user_id = from_context(AuthUserId, scope=Scope.ACTION)

    @provide(scope=Scope.APP)
    def argon(self) -> PasswordHasher:
        return PasswordHasher()

    @provide(scope=Scope.ACTION)
    def idp(self, auth_user_id: AuthUserId, uow: UoW) -> IdProvider:
        return UserIdProvider(auth_user_id, uow)


def adapter_provider() -> AdapterProvider:
    provider = AdapterProvider()
    provider.provide(get_engine, scope=Scope.APP)
    provider.provide(get_sessionmaker, scope=Scope.APP)
    provider.provide(get_session, provides=AnyOf[Session, UoW], scope=Scope.REQUEST)

    return provider
