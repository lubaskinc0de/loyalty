import os
from collections.abc import AsyncIterator, Iterable, Iterator

import aiohttp
import pytest
from aiohttp import ClientSession
from dishka import Container
from sqlalchemy import text
from sqlalchemy.orm import Session

from loyalty.bootstrap.di.container import get_container
from tests.e2e.api_client import TestAPIClient


@pytest.fixture
def container() -> Iterator[Container]:
    container = get_container()
    yield container
    container.close()


@pytest.fixture
def session(container: Container) -> Iterator[Session]:
    with container() as r:
        yield (r.get(Session))


@pytest.fixture(autouse=True)
def gracefully_teardown(
    session: Session,
) -> Iterable[None]:
    yield
    # drop db
    session.execute(
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
    session.commit()


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
