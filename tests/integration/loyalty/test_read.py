from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.application.loyalty.create import LoyaltyForm
from loyalty.application.loyalty.dto import LoyaltyData
from loyalty.application.loyalty.update import UpdateLoyaltyForm
from loyalty.domain.shared_types import Gender, LoyaltyTimeFrame
from tests.conftest import BusinessUser, ClientUser


@pytest.mark.parametrize(
    (
        "time_frame",
        "is_active",
    ),
    [
        (LoyaltyTimeFrame.CURRENT, None),
        (LoyaltyTimeFrame.ALL, None),
        (LoyaltyTimeFrame.ALL, False),
    ],
)
async def test_many_by_business_id(
    api_client: LoyaltyClient,
    business: BusinessUser,
    loyalty_form: LoyaltyForm,
    another_business: BusinessUser,
    update_loyalty_form: UpdateLoyaltyForm,
    time_frame: LoyaltyTimeFrame,
    is_active: bool,
) -> None:
    src_business, _, business_token = business
    another_business_token = another_business[2]

    api_client.authorize(business_token)
    await api_client.create_loyalty(loyalty_form)

    loyalty_form.name = "Aaa"
    start_datetime = datetime(
        year=datetime.now(tz=UTC).year + 1,
        month=datetime.now(tz=UTC).month,
        day=datetime.now(tz=UTC).day,
        tzinfo=UTC,
    )
    loyalty_form.starts_at = start_datetime

    resp_create = await api_client.create_loyalty(loyalty_form)

    assert resp_create.content is not None

    if is_active is not None:
        update_loyalty_form.is_active = is_active
        await api_client.update_loyalty(resp_create.content.loyalty_id, update_loyalty_form)

    api_client.authorize(another_business_token)
    loyalty_form.name = "Bbb"
    await api_client.create_loyalty(loyalty_form)

    api_client.authorize(business_token)
    loyalties = (
        (
            await api_client.read_loyalties(
                time_frame=time_frame,
                business_id=src_business.business_id,
                active=is_active,
            )
        )
        .unwrap()
        .loyalties
    )

    for loyalty in loyalties:
        if time_frame == LoyaltyTimeFrame.CURRENT:
            assert loyalty.starts_at < datetime.now(tz=UTC) < loyalty.ends_at
        if is_active is True:
            assert loyalty.is_active == is_active


@pytest.mark.parametrize(
    ("limit", "offset"),
    [
        (-1, 0),
        (10, -1),
    ],
)
async def test_many_wrong_limit(
    api_client: LoyaltyClient,
    business: BusinessUser,
    loyalty_form: LoyaltyForm,
    limit: int,
    offset: int,
) -> None:
    src_business, _, business_token = business

    api_client.authorize(business_token)
    (await api_client.create_loyalty(loyalty_form)).unwrap()

    loyalty_form.name = "Aaa"
    (await api_client.create_loyalty(loyalty_form)).unwrap()

    (
        await api_client.read_loyalties(
            business_id=src_business.business_id,
            limit=limit,
            offset=offset,
        )
    ).except_status(422)


@pytest.mark.parametrize(
    ("time_frame", "is_active"),
    [
        (LoyaltyTimeFrame.CURRENT, None),
        (LoyaltyTimeFrame.ALL, None),
        (LoyaltyTimeFrame.ALL, False),
    ],
)
async def test_many_by_another_business_id(
    api_client: LoyaltyClient,
    business: BusinessUser,
    loyalty_form: LoyaltyForm,
    another_business: BusinessUser,
    time_frame: LoyaltyTimeFrame,
    is_active: bool,
) -> None:
    _, _, business_token = business
    src_another_business, _, another_business_token = another_business

    api_client.authorize(another_business_token)
    await api_client.create_loyalty(loyalty_form)

    loyalty_form.name = "Aaa"

    await api_client.create_loyalty(loyalty_form)

    api_client.authorize(business_token)
    (
        await api_client.read_loyalties(
            business_id=src_another_business.business_id,
            time_frame=time_frame,
            active=is_active,
        )
    ).except_status(403)


@pytest.mark.parametrize(
    ("loyalty_gender_value", "enable_business_filter"),
    [
        (None, False),
        (Gender.FEMALE, False),
        (None, True),
    ],
)
async def test_many_client(
    api_client: LoyaltyClient,
    business: BusinessUser,
    another_client: ClientUser,
    another_business: BusinessUser,
    loyalty_form: LoyaltyForm,
    loyalty_gender_value: Gender | None,
    enable_business_filter: bool,
) -> None:
    src_business, _, business_token = business
    another_business_token = another_business[2]
    client_token = another_client[2]

    api_client.authorize(business_token)
    await api_client.create_loyalty(loyalty_form)

    loyalty_form.name = "Aaa"

    await api_client.create_loyalty(loyalty_form)

    api_client.authorize(another_business_token)
    loyalty_form.name = "Bbb"
    loyalty_form.gender = loyalty_gender_value

    await api_client.create_loyalty(loyalty_form)

    api_client.authorize(client_token)
    loyalties = (
        (
            await api_client.read_loyalties(
                business_id=None if enable_business_filter is False else src_business.business_id,
            )
        )
        .unwrap()
        .loyalties
    )

    for loyalty in loyalties:
        if loyalty_gender_value:
            assert (loyalty.gender == loyalty_gender_value) or (loyalty.gender is None)
        if enable_business_filter is True:
            assert loyalty.business == src_business


async def test_ok(
    api_client: LoyaltyClient,
    business: BusinessUser,
    loyalty: LoyaltyData,
) -> None:
    token = business[2]

    api_client.authorize(token)
    read_loyalty = (await api_client.read_loyalty(loyalty.loyalty_id)).unwrap()

    assert read_loyalty == loyalty


async def test_not_found(
    api_client: LoyaltyClient,
    business: BusinessUser,
) -> None:
    token = business[2]
    api_client.authorize(token)
    (await api_client.read_loyalty(uuid4())).except_status(404)


async def test_by_client(
    api_client: LoyaltyClient,
    another_client: ClientUser,
    loyalty: LoyaltyData,
) -> None:
    client_token = another_client[2]

    api_client.authorize(client_token)
    read_loyalty = (await api_client.read_loyalty(loyalty.loyalty_id)).unwrap()

    assert read_loyalty == loyalty


@pytest.mark.parametrize(
    ("time_frame", "is_active"),
    [
        (LoyaltyTimeFrame.CURRENT, False),
        (LoyaltyTimeFrame.ALL, True),
    ],
)
async def test_many_client_access_denied(
    api_client: LoyaltyClient,
    business: BusinessUser,
    loyalty_form: LoyaltyForm,
    update_loyalty_form: UpdateLoyaltyForm,
    another_client: ClientUser,
    time_frame: LoyaltyTimeFrame,
    is_active: bool,
) -> None:
    business_token = business[2]
    client_token = another_client[2]

    api_client.authorize(business_token)
    await api_client.create_loyalty(loyalty_form)

    loyalty_form.name = "Aaa"
    start_datetime = datetime(
        year=datetime.now(tz=UTC).year + (1 if time_frame == LoyaltyTimeFrame.ALL else -2),
        month=datetime.now(tz=UTC).month,
        day=datetime.now(tz=UTC).day,
        tzinfo=UTC,
    )
    loyalty_form.starts_at = start_datetime

    loyalty_id = (await api_client.create_loyalty(loyalty_form)).unwrap().loyalty_id

    update_loyalty_form.is_active = is_active
    await api_client.update_loyalty(loyalty_id, update_loyalty_form)

    api_client.authorize(client_token)
    (await api_client.read_loyalties(time_frame=time_frame, active=is_active)).except_status(403)


async def test_unauthorized(
    api_client: LoyaltyClient,
    loyalty: LoyaltyData,
) -> None:
    api_client.reset_authorization()
    (await api_client.read_loyalty(loyalty.loyalty_id)).except_status(401)


@pytest.mark.parametrize(
    ("enable_business_filter", "time_frame", "is_active", "expected_status"),
    [
        (False, LoyaltyTimeFrame.CURRENT, True, 200),
        (True, LoyaltyTimeFrame.CURRENT, None, 403),
        (False, LoyaltyTimeFrame.ALL, True, 403),
        (False, LoyaltyTimeFrame.CURRENT, None, 403),
    ],
)
async def test_unauthorized_many(
    business: BusinessUser,
    api_client: LoyaltyClient,
    loyalty_form: LoyaltyForm,
    enable_business_filter: bool,
    time_frame: LoyaltyTimeFrame,
    is_active: bool | None,
    expected_status: int,
) -> None:
    src_business, _, token = business

    api_client.authorize(token)
    (await api_client.create_loyalty(loyalty_form)).unwrap()

    loyalty_form.name = "really unique name"
    (await api_client.create_loyalty(loyalty_form)).unwrap()

    loyalty_form.name = "really super unique name"
    loyalty_form.starts_at = datetime.now(tz=UTC) - timedelta(weeks=10)
    loyalty_form.ends_at = datetime.now(tz=UTC) - timedelta(weeks=5)
    (await api_client.create_loyalty(loyalty_form)).unwrap()

    business_id = src_business.business_id if enable_business_filter is True else None

    api_client.reset_authorization()
    loyalties_response = (
        await api_client.read_loyalties(business_id=business_id, time_frame=time_frame, active=is_active)
    ).except_status(expected_status)

    if expected_status == 200:
        for loyalty in loyalties_response.unwrap().loyalties:
            assert loyalty.starts_at < datetime.now(tz=UTC) < loyalty.ends_at
            assert loyalty.is_active == is_active
