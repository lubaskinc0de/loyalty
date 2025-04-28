import os
from collections.abc import AsyncIterator, Iterable, Iterator
from datetime import datetime

import aiohttp
import pytest
from aiohttp import ClientSession
from dishka import Container
from pydantic_extra_types.coordinate import Latitude, Longitude
from sqlalchemy import text
from sqlalchemy.orm import Session

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.adapters.auth.provider import WebUserCredentials
from loyalty.application.business.create import BusinessForm
from loyalty.application.business_branch.create import BusinessBranchForm
from loyalty.application.client.create import ClientForm
from loyalty.application.data_model.loyalty import LoyaltyForm
from loyalty.application.shared_types import RussianPhoneNumber
from loyalty.bootstrap.di.container import get_container
from loyalty.domain.entity.business import Business
from loyalty.domain.entity.client import Client
from loyalty.domain.entity.user import User
from loyalty.domain.shared_types import Gender


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
def api_client(http_session: ClientSession) -> LoyaltyClient:
    return LoyaltyClient(session=http_session)


@pytest.fixture
def client_form() -> ClientForm:
    return ClientForm(
        full_name="Ilya Lyubavskiy",
        age=20,
        lat=Latitude(55.7522),
        lon=Longitude(37.6156),
        gender=Gender.MALE,
        phone=RussianPhoneNumber("+79281778645"),
    )


@pytest.fixture
def business_form() -> BusinessForm:
    return BusinessForm(
        name="Ilya Lyubavskiy Business",
        contact_phone=RussianPhoneNumber("+79281778645"),
        contact_email="structnull@yandex.ru",
    )


@pytest.fixture
def another_business_form() -> BusinessForm:
    return BusinessForm(
        name="THIS BUSINESS IS A SCAM",
        contact_phone=RussianPhoneNumber("+79234567890"),
        contact_email="scamer@scam.scam",
    )


@pytest.fixture
def business_branch_form() -> BusinessBranchForm:
    return BusinessBranchForm(
        name="Grocery Store №2",
        lon=Longitude(10.6531),
        lat=Latitude(10.1356),
        contact_phone=RussianPhoneNumber("+79281778645"),
    )


@pytest.fixture
def loyalty_form() -> LoyaltyForm:
    start_datetime = datetime.now()
    start_datetime.year += 1
    end_datetime = start_datetime
    end_datetime.year += 1

    return LoyaltyForm(
        name="Скидка на крутейшую газировку",
        description='Скидка на Dr.Pepper "Вишня" 0.355мл',
        starts_at=start_datetime,
        ends_at=end_datetime,
        money_per_bonus=10,
        min_age=12,
        max_age=30,
        is_active=False,
        gender=Gender.MALE,
    )


@pytest.fixture
def auth_data() -> WebUserCredentials:
    return WebUserCredentials(
        username="lubaskin business",
        password="coolpassw",  # noqa: S106
    )


@pytest.fixture
def another_auth_data() -> WebUserCredentials:
    return WebUserCredentials(
        username="NOT lubaskin business",
        password="thispasswordsucks",  # noqa: S106
    )


type AuthorizedUser = tuple[User, str]


async def create_user(
    api_client: LoyaltyClient,
    auth_data: WebUserCredentials,
) -> User:
    resp_user = await api_client.web_sign_up(auth_data)
    assert resp_user.http_response.status == 200
    assert resp_user.content is not None

    user = resp_user.content
    return user


async def create_authorized_user(
    api_client: LoyaltyClient,
    auth_data: WebUserCredentials,
) -> AuthorizedUser:
    user = await create_user(api_client, auth_data)
    resp_login = await api_client.login(auth_data)
    assert resp_login.http_response.status == 200
    assert resp_login.content is not None

    token = resp_login.content.token
    return user, token


@pytest.fixture
async def user(
    api_client: LoyaltyClient,
    auth_data: WebUserCredentials,
) -> User:
    return await create_user(api_client, auth_data)


@pytest.fixture
async def authorized_user(
    api_client: LoyaltyClient,
    auth_data: WebUserCredentials,
) -> AuthorizedUser:
    return await create_authorized_user(api_client, auth_data)


@pytest.fixture
async def another_authorized_user(
    api_client: LoyaltyClient,
    another_auth_data: WebUserCredentials,
) -> AuthorizedUser:
    return await create_authorized_user(api_client, another_auth_data)


type ClientUser = tuple[Client, *AuthorizedUser]


async def create_client(
    api_client: LoyaltyClient,
    client_form: ClientForm,
    authorized_user: AuthorizedUser,
) -> ClientUser:
    user, token = authorized_user
    resp_create = await api_client.create_client(client_form, token)
    assert resp_create.http_response.status == 204

    resp_client = await api_client.read_client(token)
    assert resp_client.content is not None

    client = resp_client.content
    return client, user, token


@pytest.fixture
async def client(
    api_client: LoyaltyClient,
    client_form: ClientForm,
    authorized_user: AuthorizedUser,
) -> ClientUser:
    return await create_client(api_client, client_form, authorized_user)


type BusinessUser = tuple[Business, *AuthorizedUser]


async def create_business(
    api_client: LoyaltyClient,
    business_form: BusinessForm,
    authorized_user: AuthorizedUser,
) -> BusinessUser:
    user, token = authorized_user
    resp_create = await api_client.create_business(business_form, token)
    assert resp_create.http_response.status == 204

    resp_userinfo = await api_client.read_user(token)
    assert resp_userinfo.http_response.status == 200
    assert resp_userinfo.content is not None
    assert resp_userinfo.content.business is not None

    business_id = resp_userinfo.content.business.business_id
    resp_business = await api_client.read_business(business_id, token)

    assert resp_business.content is not None
    return resp_business.content, user, token


@pytest.fixture
async def business(
    api_client: LoyaltyClient,
    business_form: BusinessForm,
    authorized_user: AuthorizedUser,
) -> BusinessUser:
    return await create_business(api_client, business_form, authorized_user)


@pytest.fixture
async def another_business(
    api_client: LoyaltyClient,
    another_business_form: BusinessForm,
    another_authorized_user: AuthorizedUser,
) -> BusinessUser:
    return await create_business(api_client, another_business_form, another_authorized_user)
