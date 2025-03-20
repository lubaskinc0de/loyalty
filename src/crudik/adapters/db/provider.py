import logging
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from crudik.adapters.config_loader import DBConnectionConfig


async def get_engine(config: DBConnectionConfig) -> AsyncIterator[AsyncEngine]:
    connection_url = config.postgres_conn_url

    engine = create_async_engine(
        connection_url,
        future=True,
    )

    logging.debug("Engine was created.")

    yield engine

    await engine.dispose()

    logging.debug("Engine was disposed.")


async def get_async_sessionmaker(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    logging.debug("sessionmaker initialized")

    return session_factory


async def get_async_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncIterator[AsyncSession]:
    async with session_factory() as session:
        yield session
