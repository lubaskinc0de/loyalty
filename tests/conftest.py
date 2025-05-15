import asyncio
import os
from collections.abc import AsyncIterator, Coroutine, Iterable, Iterator
from datetime import UTC, datetime, timedelta
from decimal import ROUND_DOWN, Decimal
from importlib.resources import as_file, files
from importlib.resources.abc import Traversable
from pathlib import Path
from typing import Any

import aiohttp
import pytest
from aiohttp import ClientSession
from dishka import Container
from pydantic_extra_types.coordinate import Latitude, Longitude
from sqlalchemy import text
from sqlalchemy.orm import Session

import tests.assets
from loyalty.adapters.api_client import APIResponse, LoyaltyClient
from loyalty.adapters.auth.provider import WebUserCredentials
from loyalty.application.business.create import BusinessForm
from loyalty.application.client.create import ClientForm
from loyalty.application.data_model.business_branch import BusinessBranchData, BusinessBranchForm
from loyalty.application.loyalty.create import LoyaltyForm
from loyalty.application.loyalty.dto import LoyaltyData
from loyalty.application.loyalty.update import UpdateLoyaltyForm
from loyalty.application.membership.create import MembershipForm
from loyalty.application.membership.dto import MembershipData
from loyalty.application.payment.create import PaymentForm, PaymentId
from loyalty.application.shared_types import RussianPhoneNumber
from loyalty.bootstrap.di.container import get_container
from loyalty.domain.entity.business import Business
from loyalty.domain.entity.client import Client
from loyalty.domain.entity.payment import Payment
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


def relative_url(url: str) -> str:
    parts = url.split("/")
    return "/" + parts[3] + "/" + "/".join(parts[4:])


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
def another_business_branch_form() -> BusinessBranchForm:
    return BusinessBranchForm(
        name="Grocery Store №3",
        lon=Longitude(10.6531),
        lat=Latitude(10.1356),
        contact_phone=RussianPhoneNumber("+79281778646"),
    )


LOYALTY_MIN_AGE = 16
LOYALTY_MAX_AGE = 30


@pytest.fixture
def loyalty_form(branch: BusinessBranchData) -> LoyaltyForm:
    start_datetime = datetime.now(tz=UTC) - timedelta(days=365)
    end_datetime = datetime.now(tz=UTC) + timedelta(days=365)
    return LoyaltyForm(
        name="Скидка на крутейшую газировку",
        description='Скидка на Dr.Pepper "Вишня" 0.355мл',
        starts_at=start_datetime,
        ends_at=end_datetime,
        money_per_bonus=Decimal("10"),
        money_for_bonus=Decimal("0.1"),
        min_age=16,
        max_age=30,
        gender=None,
        business_branches_id_list=[branch.business_branch_id],
    )


@pytest.fixture
def update_loyalty_form() -> UpdateLoyaltyForm:
    start_datetime = datetime.now(tz=UTC) - timedelta(days=365)
    end_datetime = datetime.now(tz=UTC) + timedelta(days=365)
    return UpdateLoyaltyForm(
        name="Скидка на крутейшую газировкуfff",
        description="не, маунтин дью круче",
        starts_at=start_datetime,
        ends_at=end_datetime,
        money_per_bonus=Decimal("10"),
        money_for_bonus=Decimal("0.1"),
        is_active=True,
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
    api_client.authorize(token)

    resp_create = await api_client.create_client(client_form)
    assert resp_create.http_response.status == 204

    resp_client = await api_client.read_client()
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


@pytest.fixture
async def another_client(
    api_client: LoyaltyClient,
    client_form: ClientForm,
) -> ClientUser:
    client_data = await create_authorized_user(
        api_client,
        WebUserCredentials(
            username="someosskemsf",
            password="someeeeepasssswwwwf",  # noqa: S106
        ),
    )
    return await create_client(api_client, client_form, client_data)


type BusinessUser = tuple[Business, *AuthorizedUser]


async def create_business(
    api_client: LoyaltyClient,
    business_form: BusinessForm,
    authorized_user: AuthorizedUser,
) -> BusinessUser:
    user, token = authorized_user
    api_client.authorize(token)

    resp_create = await api_client.create_business(business_form)
    assert resp_create.http_response.status == 204

    resp_userinfo = await api_client.read_user()
    assert resp_userinfo.http_response.status == 200
    assert resp_userinfo.content is not None
    assert resp_userinfo.content.business is not None

    business_id = resp_userinfo.content.business.business_id
    resp_business = await api_client.read_business(business_id)

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


@pytest.fixture
async def loyalty(api_client: LoyaltyClient, business: BusinessUser, loyalty_form: LoyaltyForm) -> LoyaltyData:
    api_client.authorize(business[2])
    loyalty_form.name = "Test_name_of_loyalty___"
    loyalty_id = (await api_client.create_loyalty(loyalty_form)).unwrap()
    return (await api_client.read_loyalty(loyalty_id.loyalty_id)).unwrap()


@pytest.fixture
async def another_loyalty(
    api_client: LoyaltyClient,
    another_business: BusinessUser,
    loyalty_form: LoyaltyForm,
) -> LoyaltyData:
    api_client.authorize(another_business[2])
    loyalty_form.name = "Test_name_of_loyalty___2"
    loyalty_form.business_branches_id_list = []
    loyalty_id = (await api_client.create_loyalty(loyalty_form)).unwrap()
    return (await api_client.read_loyalty(loyalty_id.loyalty_id)).unwrap()


@pytest.fixture
async def membership(api_client: LoyaltyClient, loyalty: LoyaltyData, client: ClientUser) -> MembershipData:
    api_client.authorize(client[2])
    membership_id = (
        (
            await api_client.create_membership(
                MembershipForm(
                    loyalty_id=loyalty.loyalty_id,
                ),
            )
        )
        .unwrap()
        .membership_id
    )
    return (await api_client.read_membership(membership_id)).unwrap()


@pytest.fixture
async def another_membership(
    api_client: LoyaltyClient,
    another_loyalty: LoyaltyData,
    another_client: ClientUser,
) -> MembershipData:
    api_client.authorize(another_client[2])
    membership_id = (
        (
            await api_client.create_membership(
                MembershipForm(
                    loyalty_id=another_loyalty.loyalty_id,
                ),
            )
        )
        .unwrap()
        .membership_id
    )
    return (await api_client.read_membership(membership_id)).unwrap()


@pytest.fixture
async def loyalties(
    api_client: LoyaltyClient,
    business: BusinessUser,
    loyalty_form: LoyaltyForm,
) -> list[LoyaltyData]:
    names = [
        "aaaa",
        "bbbbb",
        "ccccc",
    ]
    forms = [
        loyalty_form.model_copy(
            update={
                "name": name,
            },
        )
        for name in names
    ]
    api_client.authorize(business[2])
    loyalty_ids = [
        x.unwrap().loyalty_id for x in await asyncio.gather(*[api_client.create_loyalty(form) for form in forms])
    ]
    loyalties = [
        x.unwrap() for x in await asyncio.gather(*[api_client.read_loyalty(loyalty_id) for loyalty_id in loyalty_ids])
    ]
    return loyalties


@pytest.fixture
async def branch(
    api_client: LoyaltyClient,
    business: BusinessUser,
    business_branch_form: BusinessBranchForm,
) -> BusinessBranchData:
    api_client.authorize(business[2])

    branch_id = (await api_client.create_business_branch(business_branch_form)).unwrap().branch_id
    branch = (await api_client.read_business_branch(branch_id)).unwrap()

    return branch


@pytest.fixture
async def another_branch(
    api_client: LoyaltyClient,
    business: BusinessUser,
    another_business_branch_form: BusinessBranchForm,
) -> BusinessBranchData:
    api_client.authorize(business[2])

    branch_id = (await api_client.create_business_branch(another_business_branch_form)).unwrap().branch_id
    branch = (await api_client.read_business_branch(branch_id)).unwrap()

    return branch


@pytest.fixture
async def another_business_branch(
    api_client: LoyaltyClient,
    another_business: BusinessUser,
    another_business_branch_form: BusinessBranchForm,
) -> BusinessBranchData:
    api_client.authorize(another_business[2])

    branch_id = (await api_client.create_business_branch(another_business_branch_form)).unwrap().branch_id
    branch = (await api_client.read_business_branch(branch_id)).unwrap()

    return branch


@pytest.fixture
async def bonus_balance(
    api_client: LoyaltyClient,
    membership: MembershipData,
    client: ClientUser,
    business: BusinessUser,
    branch: BusinessBranchData,
) -> Decimal:
    api_client.authorize(business[2])
    payments = [Decimal(x) for x in ["100.67", "254.87", "1000.78"]]

    tasks: list[Coroutine[Any, Any, APIResponse[PaymentId]]] = []
    tasks_read: list[Coroutine[Any, Any, APIResponse[Payment]]] = []
    for summ in payments:
        payment_form = PaymentForm(
            payment_sum=summ,
            membership_id=membership.membership_id,
            business_branch_id=branch.business_branch_id,
            client_id=client[0].client_id,
        )
        tasks.append(api_client.create_payment(payment_form))

    for create_request in await asyncio.gather(*tasks):
        tasks_read.append(api_client.read_payment(create_request.except_status(200).unwrap().payment_id))  # noqa: PERF401

    summa = Decimal(sum([x.unwrap().bonus_income for x in await asyncio.gather(*tasks_read)]))
    api_client.authorize(client[2])
    balance = (await api_client.read_bonuses(membership.membership_id)).unwrap().balance

    assert summa.quantize(Decimal("0.01"), ROUND_DOWN) == balance
    return balance


@pytest.fixture
async def payment(
    api_client: LoyaltyClient,
    membership: MembershipData,
    client: ClientUser,
    business: BusinessUser,
    branch: BusinessBranchData,
) -> Payment:
    client_obj, _, _ = client
    _, _, token = business
    payment_sum = Decimal("100.05")
    api_client.authorize(token)
    form = PaymentForm(
        payment_sum=payment_sum,
        membership_id=membership.membership_id,
        business_branch_id=branch.business_branch_id,
        client_id=client_obj.client_id,
    )

    payment_id = (await api_client.create_payment(form)).unwrap().payment_id
    return (await api_client.read_payment(payment_id)).unwrap()


@pytest.fixture
async def another_payment(
    api_client: LoyaltyClient,
    another_membership: MembershipData,
    another_client: ClientUser,
    business: BusinessUser,
    branch: BusinessBranchData,
) -> Payment:
    client_obj, _, _ = another_client
    _, _, token = business
    payment_sum = Decimal("2848.05")
    api_client.authorize(token)
    form = PaymentForm(
        payment_sum=payment_sum,
        membership_id=another_membership.membership_id,
        business_branch_id=branch.business_branch_id,
        client_id=client_obj.client_id,
    )

    payment_id = (await api_client.create_payment(form)).unwrap().payment_id
    return (await api_client.read_payment(payment_id)).unwrap()


@pytest.fixture
def assets() -> Traversable:
    return files(tests.assets)


@pytest.fixture
def image_file(assets: Traversable) -> Iterable[Path]:
    with as_file(assets.joinpath("ya.jpg")) as path:
        yield path


@pytest.fixture
def text_file(assets: Traversable) -> Iterable[Path]:
    with as_file(assets.joinpath("hello.txt")) as path:
        yield path


@pytest.fixture
def without_extension_file(assets: Traversable) -> Iterable[Path]:
    with as_file(assets.joinpath("hello")) as path:
        yield path
