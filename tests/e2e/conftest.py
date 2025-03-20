import os
from collections.abc import AsyncIterable, AsyncIterator

import aiohttp
import pytest
from aiohttp import ClientSession
from dishka import AsyncContainer
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from crudik.bootstrap.di.container import get_async_container
from tests.e2e.api_client import TestAPIClient


@pytest.fixture
async def container() -> AsyncIterator[AsyncContainer]:
    container = get_async_container()
    yield container
    await container.close()


@pytest.fixture
async def session(container: AsyncContainer) -> AsyncIterator[AsyncSession]:
    async with container() as r:
        yield (await r.get(AsyncSession))


@pytest.fixture
async def redis(container: AsyncContainer) -> Redis:
    return await container.get(Redis)


@pytest.fixture(autouse=True)
async def gracefully_teardown(
    session: AsyncSession,
) -> AsyncIterable[None]:
    yield
    await session.execute(
        text("""
            DO $$
            DECLARE
                tb text;
            BEGIN
                FOR tb IN (
                    SELECT tablename
                    FROM pg_catalog.pg_tables
                    WHERE schemaname = 'public'
                      AND tablename != 'alembic_version'
                )
                LOOP
                    EXECUTE 'TRUNCATE TABLE ' || tb || ' CASCADE';
                END LOOP;
            END $$;
        """),
    )
    await session.commit()


@pytest.fixture
async def http_session(base_url: str) -> AsyncIterator[ClientSession]:
    async with aiohttp.ClientSession(base_url=base_url) as session:
        yield session


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.environ["API_URL"]


@pytest.fixture
def client(http_session: ClientSession) -> TestAPIClient:
    return TestAPIClient(session=http_session)
