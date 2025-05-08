from uuid import uuid4

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.application.loyalty.update import UpdateLoyaltyForm
from loyalty.domain.entity.loyalty import Loyalty
from tests.conftest import BusinessUser, ClientUser


async def test_ok(
    api_client: LoyaltyClient,
    business: BusinessUser,
    loyalty: Loyalty,
    update_loyalty_form: UpdateLoyaltyForm,
) -> None:
    token = business[2]
    api_client.authorize(token)

    (
        await api_client.update_loyalty(
            loyalty.loyalty_id,
            update_loyalty_form,
        )
    ).except_status(204)

    updated_loyalty = (await api_client.read_loyalty(loyalty.loyalty_id)).unwrap()

    assert updated_loyalty.description == update_loyalty_form.description
    assert updated_loyalty.is_active == update_loyalty_form.is_active

    assert updated_loyalty.name == update_loyalty_form.name
    assert updated_loyalty.starts_at == update_loyalty_form.starts_at
    assert updated_loyalty.ends_at == update_loyalty_form.ends_at
    assert updated_loyalty.money_per_bonus == update_loyalty_form.money_per_bonus


async def test_not_found(
    api_client: LoyaltyClient,
    business: BusinessUser,
    update_loyalty_form: UpdateLoyaltyForm,
) -> None:
    token = business[2]
    api_client.authorize(token)
    (await api_client.update_loyalty(uuid4(), update_loyalty_form)).except_status(404)


async def test_another_business(
    api_client: LoyaltyClient,
    another_business: BusinessUser,
    loyalty: Loyalty,
    update_loyalty_form: UpdateLoyaltyForm,
) -> None:
    another_business_token = another_business[2]

    api_client.authorize(another_business_token)
    (
        await api_client.update_loyalty(
            loyalty.loyalty_id,
            update_loyalty_form,
        )
    ).except_status(403)


async def test_by_client(
    api_client: LoyaltyClient,
    loyalty: Loyalty,
    another_client: ClientUser,
    update_loyalty_form: UpdateLoyaltyForm,
) -> None:
    client_token = another_client[2]

    api_client.authorize(client_token)
    update_loyalty_form.name = "!!!"
    (await api_client.update_loyalty(loyalty.loyalty_id, update_loyalty_form)).except_status(403)


async def test_unauthorized(
    api_client: LoyaltyClient,
    loyalty: Loyalty,
    update_loyalty_form: UpdateLoyaltyForm,
) -> None:
    api_client.reset_authorization()
    (await api_client.update_loyalty(loyalty.loyalty_id, update_loyalty_form)).except_status(401)
