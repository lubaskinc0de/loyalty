from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

import pytest

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.application.client.create import ClientForm
from loyalty.application.loyalty.create import LoyaltyForm
from loyalty.application.loyalty.dto import LoyaltyData
from loyalty.application.loyalty.update import UpdateLoyaltyForm
from loyalty.application.membership.create import MembershipForm
from loyalty.domain.shared_types import Gender
from tests.conftest import LOYALTY_MAX_AGE, LOYALTY_MIN_AGE, AuthorizedUser, BusinessUser, ClientUser, create_client


async def test_ok(api_client: LoyaltyClient, client: ClientUser, loyalty: LoyaltyData) -> None:
    api_client.authorize(client[2])
    (
        await api_client.create_membership(
            MembershipForm(
                loyalty_id=loyalty.loyalty_id,
            ),
        )
    ).except_status(200)


async def test_as_business(api_client: LoyaltyClient, business: BusinessUser, loyalty: LoyaltyData) -> None:
    api_client.authorize(business[2])
    (
        await api_client.create_membership(
            MembershipForm(
                loyalty_id=loyalty.loyalty_id,
            ),
        )
    ).except_status(403)


async def test_not_exist_loyalty(api_client: LoyaltyClient, client: ClientUser) -> None:
    api_client.authorize(client[2])
    (
        await api_client.create_membership(
            MembershipForm(
                loyalty_id=uuid4(),
            ),
        )
    ).except_status(404)


async def test_twice(api_client: LoyaltyClient, client: ClientUser, loyalty: LoyaltyData) -> None:
    api_client.authorize(client[2])
    (
        await api_client.create_membership(
            MembershipForm(
                loyalty_id=loyalty.loyalty_id,
            ),
        )
    ).except_status(200)
    (
        await api_client.create_membership(
            MembershipForm(
                loyalty_id=loyalty.loyalty_id,
            ),
        )
    ).except_status(409)


@pytest.mark.parametrize(
    ("param", "deviation"),
    [
        ("age", LOYALTY_MIN_AGE - 1),
        ("age", LOYALTY_MAX_AGE + 1),
    ],
)
async def test_targeting_mismatch(
    api_client: LoyaltyClient,
    client_form: ClientForm,
    authorized_user: AuthorizedUser,
    loyalty: LoyaltyData,
    param: str,
    deviation: Any,
) -> None:
    setattr(client_form, param, deviation)
    client = await create_client(api_client, client_form, authorized_user)
    api_client.authorize(client[2])
    (
        await api_client.create_membership(
            MembershipForm(
                loyalty_id=loyalty.loyalty_id,
            ),
        )
    ).except_status(403)


async def test_gender_mismatch(
    api_client: LoyaltyClient,
    client_form: ClientForm,
    authorized_user: AuthorizedUser,
    loyalty_form: LoyaltyForm,
    business: BusinessUser,
) -> None:
    loyalty_form.gender = Gender.MALE
    client_form.gender = Gender.FEMALE
    client = await create_client(api_client, client_form, authorized_user)
    api_client.authorize(business[2])
    loyalty_id = (await api_client.create_loyalty(loyalty_form)).unwrap().loyalty_id

    api_client.authorize(client[2])
    (
        await api_client.create_membership(
            MembershipForm(
                loyalty_id=loyalty_id,
            ),
        )
    ).except_status(403)


async def test_not_active(
    api_client: LoyaltyClient,
    client: ClientUser,
    loyalty: LoyaltyData,
    business: BusinessUser,
    update_loyalty_form: UpdateLoyaltyForm,
) -> None:
    update_loyalty_form.is_active = False
    api_client.authorize(business[2])
    (
        await api_client.update_loyalty(
            loyalty.loyalty_id,
            update_loyalty_form,
        )
    )
    api_client.authorize(client[2])
    (
        await api_client.create_membership(
            MembershipForm(
                loyalty_id=loyalty.loyalty_id,
            ),
        )
    ).except_status(403)


async def test_before_start(
    api_client: LoyaltyClient,
    client: ClientUser,
    loyalty_form: LoyaltyForm,
    business: BusinessUser,
) -> None:
    loyalty_form.starts_at = datetime.now(tz=UTC) + timedelta(weeks=1)
    api_client.authorize(business[2])

    loyalty_id = (
        (
            await api_client.create_loyalty(
                loyalty_form,
            )
        )
        .unwrap()
        .loyalty_id
    )

    api_client.authorize(client[2])
    (
        await api_client.create_membership(
            MembershipForm(
                loyalty_id=loyalty_id,
            ),
        )
    ).except_status(403)


async def test_after_end(
    api_client: LoyaltyClient,
    client: ClientUser,
    loyalty_form: LoyaltyForm,
    business: BusinessUser,
) -> None:
    loyalty_form.starts_at = datetime.now(tz=UTC) - timedelta(weeks=2)
    loyalty_form.ends_at = datetime.now(tz=UTC) - timedelta(weeks=1)

    api_client.authorize(business[2])
    loyalty_id = (
        (
            await api_client.create_loyalty(
                loyalty_form,
            )
        )
        .unwrap()
        .loyalty_id
    )

    api_client.authorize(client[2])
    (
        await api_client.create_membership(
            MembershipForm(
                loyalty_id=loyalty_id,
            ),
        )
    ).except_status(403)


async def test_unauthorized(api_client: LoyaltyClient, loyalty: LoyaltyData) -> None:
    api_client.reset_authorization()
    (
        await api_client.create_membership(
            MembershipForm(
                loyalty_id=loyalty.loyalty_id,
            ),
        )
    ).except_status(401)
