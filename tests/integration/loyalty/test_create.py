from uuid import uuid4

import pytest

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.application.loyalty.create import LoyaltyForm
from loyalty.domain.shared_types import Gender
from tests.conftest import BusinessUser, ClientUser


@pytest.mark.parametrize(
    "gender_value",
    [
        Gender.MALE,
        None,
        Gender.FEMALE,
    ],
)
async def test_ok(
    api_client: LoyaltyClient,
    business: BusinessUser,
    loyalty_form: LoyaltyForm,
    gender_value: Gender | None,
) -> None:
    src_business, _, token = business
    api_client.authorize(token)

    loyalty_form.gender = gender_value

    loyalty_id = (await api_client.create_loyalty(loyalty_form)).unwrap().loyalty_id

    created_loyalty = (await api_client.read_loyalty(loyalty_id)).unwrap()

    assert loyalty_form.name == created_loyalty.name
    assert loyalty_form.description == created_loyalty.description
    assert loyalty_form.starts_at == created_loyalty.starts_at
    assert loyalty_form.ends_at == created_loyalty.ends_at
    assert loyalty_form.money_per_bonus == created_loyalty.money_per_bonus
    assert loyalty_form.min_age == created_loyalty.min_age
    assert loyalty_form.max_age == created_loyalty.max_age
    assert loyalty_form.gender == created_loyalty.gender
    assert loyalty_form.money_for_bonus == created_loyalty.money_for_bonus
    assert loyalty_form.business_branches_id_list == [x.business_branch_id for x in created_loyalty.business_branches]
    assert src_business == created_loyalty.business


async def test_ok_without_branches(
    api_client: LoyaltyClient,
    business: BusinessUser,
    loyalty_form: LoyaltyForm,
) -> None:
    _, _, token = business
    api_client.authorize(token)

    loyalty_form.business_branches_id_list = []
    loyalty_id = (await api_client.create_loyalty(loyalty_form)).unwrap().loyalty_id
    created_loyalty = (await api_client.read_loyalty(loyalty_id)).unwrap()

    assert created_loyalty.business_branches == []


async def test_fake_business(
    api_client: LoyaltyClient,
    loyalty_form: LoyaltyForm,
) -> None:
    fake_business_token = str(uuid4())

    api_client.authorize(fake_business_token)
    (await api_client.create_loyalty(loyalty_form)).except_status(401)


async def test_not_unique_name(
    api_client: LoyaltyClient,
    loyalty_form: LoyaltyForm,
    business: BusinessUser,
) -> None:
    token = business[2]
    api_client.authorize(token)

    await api_client.create_loyalty(loyalty_form)

    (await api_client.create_loyalty(loyalty_form)).except_status(409)


async def test_by_client(
    api_client: LoyaltyClient,
    loyalty_form: LoyaltyForm,
    another_client: ClientUser,
) -> None:
    client_token = another_client[2]
    api_client.authorize(client_token)

    (await api_client.create_loyalty(loyalty_form)).except_status(403)
