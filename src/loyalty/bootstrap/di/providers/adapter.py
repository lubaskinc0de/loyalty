from dishka import Provider, Scope

from loyalty.adapters.db.provider import get_engine, get_session, get_sessionmaker


class AdapterProvider(Provider):
    ...


def adapter_provider() -> AdapterProvider:
    provider = AdapterProvider()
    provider.provide(get_engine, scope=Scope.APP)
    provider.provide(get_sessionmaker, scope=Scope.APP)
    provider.provide(get_session, scope=Scope.REQUEST)

    return provider
