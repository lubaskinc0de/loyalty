import os
from collections.abc import AsyncIterator, Iterable, Iterator

import aiohttp
import pytest
from aiohttp import ClientSession
from dishka import Container
from pydantic_extra_types.coordinate import Latitude, Longitude
from sqlalchemy import text
from sqlalchemy.orm import Session

from loyalty.application.business.create_business import BusinessForm
from loyalty.application.client.create_client import ClientForm
from loyalty.application.shared_types import RussianPhoneNumber
from loyalty.bootstrap.di.container import get_container
from loyalty.domain.entity.user import User
from loyalty.domain.shared_types import Gender
from loyalty.presentation.web.controller.sign_up_business import BusinessWebSignUpForm
from loyalty.presentation.web.controller.sign_up_client import ClientWebSignUpForm
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
def api_client(http_session: ClientSession) -> TestAPIClient:
    return TestAPIClient(session=http_session)


@pytest.fixture
def valid_client_signup_form() -> ClientWebSignUpForm:
    return ClientWebSignUpForm(
        username="lubaskin",
        password="coolpassw",  # noqa: S106
        client_data=ClientForm(
            full_name="Ilya Lyubavskiy",
            age=20,
            lat=Latitude(55.7522),
            lon=Longitude(37.6156),
            gender=Gender.MALE,
            phone=RussianPhoneNumber("+79281778645"),
        ),
    )


async def create_client(api_client: TestAPIClient, valid_client_signup_form: ClientWebSignUpForm) -> User:
    resp = await api_client.sign_up_client(valid_client_signup_form)
    assert resp.http_response.status == 200
    assert resp.content is not None

    return resp.content


@pytest.fixture
async def client(api_client: TestAPIClient, valid_client_signup_form: ClientWebSignUpForm) -> User:
    return await create_client(api_client, valid_client_signup_form)


@pytest.fixture
def valid_business_signup_form() -> BusinessWebSignUpForm:
    return BusinessWebSignUpForm(
        username="lubaskin business",
        password="coolpassw",  # noqa: S106
        business_data=BusinessForm(
            name="Ilya Lyubavskiy Business",
            lat=Latitude(55.7522),
            lon=Longitude(37.6156),
            contact_phone=RussianPhoneNumber("+79281778645"),
            contact_email="structnull@yandex.ru",
        ),
    )


async def create_business(
    api_client: TestAPIClient,
    valid_business_signup_form: BusinessWebSignUpForm,
) -> User:
    resp = await api_client.sign_up_business(valid_business_signup_form)
    assert resp.http_response.status == 200
    assert resp.content is not None

    return resp.content


@pytest.fixture
async def business(
    api_client: TestAPIClient,
    valid_business_signup_form: BusinessWebSignUpForm,
) -> User:
    return await create_business(api_client, valid_business_signup_form)
