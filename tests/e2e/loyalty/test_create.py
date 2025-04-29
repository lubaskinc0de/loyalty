from loyalty.adapters.api_client import LoyaltyClient
from loyalty.application.data_model.loyalty import LoyaltyForm
from tests.e2e.conftest import BusinessUser


async def test_ok(
    api_client: LoyaltyClient,
    business: BusinessUser,
    loyalty_form: LoyaltyForm,
) -> None:
    token = business[2]
    resp_create = await api_client.create_loyalty(loyalty_form, token)

    assert resp_create.http_response.status == 200
    assert resp_create.content is not None

    resp_read = await api_client.read_loyalty(resp_create.content.loyalty_id, token)

    created_loyalty = resp_read.content

    assert created_loyalty is not None

    assert loyalty_form.name == created_loyalty.name
    assert loyalty_form.description == created_loyalty.description
    assert loyalty_form.starts_at == created_loyalty.starts_at
    assert loyalty_form.ends_at == created_loyalty.ends_at
    assert loyalty_form.money_per_bonus == created_loyalty.money_per_bonus
    assert loyalty_form.min_age == created_loyalty.min_age
    assert loyalty_form.max_age == created_loyalty.max_age
    assert loyalty_form.is_active == created_loyalty.is_active
    assert loyalty_form.gender == created_loyalty.gender


async def test_ok_without_gender(
    api_client: LoyaltyClient,
    business: BusinessUser,
    loyalty_form: LoyaltyForm,
) -> None:
    token = business[2]
    loyalty_form.gender = None

    resp_create = await api_client.create_loyalty(loyalty_form, token)

    assert resp_create.http_response.status == 200
    assert resp_create.content is not None

    resp_read = await api_client.read_loyalty(resp_create.content.loyalty_id, token)

    created_loyalty = resp_read.content

    assert created_loyalty is not None

    assert loyalty_form.name == created_loyalty.name
    assert loyalty_form.description == created_loyalty.description
    assert loyalty_form.starts_at == created_loyalty.starts_at
    assert loyalty_form.ends_at == created_loyalty.ends_at
    assert loyalty_form.money_per_bonus == created_loyalty.money_per_bonus
    assert loyalty_form.min_age == created_loyalty.min_age
    assert loyalty_form.max_age == created_loyalty.max_age
    assert loyalty_form.is_active == created_loyalty.is_active
    assert created_loyalty.gender is None
