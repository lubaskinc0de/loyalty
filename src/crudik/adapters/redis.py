from redis.asyncio import Redis


class RedisStorage:
    def __init__(self, redis_connection: Redis) -> None:
        self.redis = redis_connection

    async def get(self, key: str) -> str | None:
        value = await self.redis.get(key)
        return value.decode("utf-8") if value else None

    async def set(self, key: str, value: str) -> None:
        await self.redis.set(key, value)
