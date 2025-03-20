from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from crudik.adapters.config_loader import DBConnectionConfig
from crudik.adapters.db.provider import get_async_session, get_async_sessionmaker, get_engine
from crudik.adapters.redis import RedisStorage


class AdapterProvider(Provider):
    redis_storage = provide(RedisStorage, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def redis_client(self, config: DBConnectionConfig) -> Redis:
        return Redis(
            host=config.redis_host,
            port=config.redis_port,
            db=0,
        )


def adapter_provider() -> AdapterProvider:
    provider = AdapterProvider()
    provider.provide(get_engine, scope=Scope.APP)
    provider.provide(get_async_sessionmaker, scope=Scope.APP)
    provider.provide(get_async_session, scope=Scope.REQUEST)

    return provider
