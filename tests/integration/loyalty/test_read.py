from datetime import UTC, datetime
from uuid import uuid4

import pytest

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.adapters.auth.provider import WebUserCredentials
from loyalty.application.client.create import ClientForm
from loyalty.application.loyalty.create import LoyaltyForm
from loyalty.application.loyalty.update import UpdateLoyaltyForm
from loyalty.domain.shared_types import Gender, LoyaltyTimeFrame
from tests.conftest import BusinessUser, create_authorized_user, create_client


@pytest.mark.parametrize(
    ("time_frame", "is_active", "expected_result"),
    [
        (LoyaltyTimeFrame.CURRENT, None, 1),
        (LoyaltyTimeFrame.ALL, None, 2),
        (LoyaltyTimeFrame.ALL, False, 1),
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
    expected_result: int,
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
    resp = await api_client.read_loyalties(
        time_frame=time_frame,
        business_id=src_business.business_id,
        active=is_active,
    )

    assert resp.http_response.status == 200
    assert resp.content is not None
    assert len(resp.content.loyalties) == expected_result


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
    await api_client.create_loyalty(loyalty_form)

    loyalty_form.name = "Aaa"
    await api_client.create_loyalty(loyalty_form)

    resp = await api_client.read_loyalties(
        business_id=src_business.business_id,
        limit=limit,
        offset=offset,
    )

    assert resp.http_response.status == 422
    assert resp.content is None


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
    resp = await api_client.read_loyalties(
        business_id=src_another_business.business_id,
        time_frame=time_frame,
        active=is_active,
    )

    assert resp.http_response.status == 403
    assert resp.content is None


@pytest.mark.parametrize(
    ("loyalty_gender_value", "enable_business_filter", "expected_result"),
    [
        (None, False, 3),
        (Gender.FEMALE, False, 2),
        (None, True, 2),
    ],
)
async def test_many_client(
    api_client: LoyaltyClient,
    business: BusinessUser,
    loyalty_form: LoyaltyForm,
    client_form: ClientForm,
    another_business: BusinessUser,
    loyalty_gender_value: Gender | None,
    enable_business_filter: bool,
    expected_result: int,
) -> None:
    src_business, _, business_token = business
    another_business_token = another_business[2]

    client_user = await create_authorized_user(
        api_client,
        WebUserCredentials(
            username="someosskems",
            password="someeeeepasssswwww",  # noqa: S106
        ),
    )
    _, _, client_token = await create_client(api_client, client_form, client_user)
    api_client.authorize(business_token)
    await api_client.create_loyalty(loyalty_form)

    loyalty_form.name = "Aaa"

    await api_client.create_loyalty(loyalty_form)

    api_client.authorize(another_business_token)
    loyalty_form.name = "Bbb"
    loyalty_form.gender = loyalty_gender_value

    await api_client.create_loyalty(loyalty_form)

    api_client.authorize(client_token)
    resp = await api_client.read_loyalties(
        business_id=None if enable_business_filter is False else src_business.business_id,
    )

    assert resp.http_response.status == 200
    assert resp.content is not None
    assert len(resp.content.loyalties) == expected_result


async def test_ok(
    api_client: LoyaltyClient,
    business: BusinessUser,
    loyalty_form: LoyaltyForm,
) -> None:
    token = business[2]
    api_client.authorize(token)

    resp_create = await api_client.create_loyalty(loyalty_form)

    assert resp_create.content is not None

    resp = await api_client.read_loyalty(resp_create.content.loyalty_id)

    assert resp.http_response.status == 200
    assert resp.content is not None


async def test_not_found(
    api_client: LoyaltyClient,
    business: BusinessUser,
) -> None:
    token = business[2]
    api_client.authorize(token)
    resp = await api_client.read_loyalty(uuid4())
    assert resp.http_response.status == 404


async def test_by_client(
    api_client: LoyaltyClient,
    business: BusinessUser,
    client_form: ClientForm,
    loyalty_form: LoyaltyForm,
) -> None:
    business_token = business[2]

    client_user = await create_authorized_user(
        api_client,
        WebUserCredentials(
            username="someosskems",
            password="someeeeepasssswwww",  # noqa: S106
        ),
    )
    _, _, client_token = await create_client(api_client, client_form, client_user)

    api_client.authorize(business_token)
    resp_create = await api_client.create_loyalty(loyalty_form)

    assert resp_create.content is not None

    api_client.authorize(client_token)
    loyalty = (await api_client.read_loyalty(resp_create.content.loyalty_id)).content

    assert loyalty is not None

    resp = await api_client.read_loyalty(loyalty.loyalty_id)

    assert resp.http_response.status == 200
    assert resp.content is not None
    assert resp.content == loyalty


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
    client_form: ClientForm,
    time_frame: LoyaltyTimeFrame,
    is_active: bool,
) -> None:
    _, _, business_token = business
    client_user = await create_authorized_user(
        api_client,
        WebUserCredentials(
            username="someosskems",
            password="someeeeepasssswwww",  # noqa: S106
        ),
    )
    _, _, client_token = await create_client(api_client, client_form, client_user)

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

    resp_create = await api_client.create_loyalty(loyalty_form)

    assert resp_create.content is not None

    update_loyalty_form.is_active = is_active
    await api_client.update_loyalty(resp_create.content.loyalty_id, update_loyalty_form)

    api_client.authorize(client_token)
    resp = await api_client.read_loyalties(time_frame=time_frame, active=is_active)

    assert resp.http_response.status == 403
    assert resp.content is None
