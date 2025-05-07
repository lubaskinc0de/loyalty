from uuid import uuid4

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.adapters.auth.provider import WebUserCredentials
from loyalty.application.client.create import ClientForm
from loyalty.application.loyalty.create import LoyaltyForm
from loyalty.application.loyalty.update import UpdateLoyaltyForm
from tests.conftest import BusinessUser, create_authorized_user, create_client


async def test_ok(
    api_client: LoyaltyClient,
    business: BusinessUser,
    loyalty_form: LoyaltyForm,
    update_loyalty_form: UpdateLoyaltyForm,
) -> None:
    token = business[2]
    api_client.authorize(token)

    resp_create = await api_client.create_loyalty(loyalty_form)

    assert resp_create.content is not None

    resp_update = await api_client.update_loyalty(
        resp_create.content.loyalty_id,
        update_loyalty_form,
    )

    assert resp_update.http_response.status == 204

    resp_read = await api_client.read_loyalty(resp_create.content.loyalty_id)

    updated_loyalty = resp_read.content

    assert updated_loyalty is not None

    assert updated_loyalty.description == update_loyalty_form.description
    assert updated_loyalty.gender == update_loyalty_form.gender
    assert updated_loyalty.is_active == update_loyalty_form.is_active

    assert updated_loyalty.name == update_loyalty_form.name
    assert updated_loyalty.starts_at == update_loyalty_form.starts_at
    assert updated_loyalty.ends_at == update_loyalty_form.ends_at
    assert updated_loyalty.money_per_bonus == update_loyalty_form.money_per_bonus
    assert updated_loyalty.min_age == update_loyalty_form.min_age
    assert updated_loyalty.max_age == update_loyalty_form.max_age


async def test_not_found(
    api_client: LoyaltyClient,
    business: BusinessUser,
    update_loyalty_form: UpdateLoyaltyForm,
) -> None:
    token = business[2]
    api_client.authorize(token)
    resp = await api_client.update_loyalty(uuid4(), update_loyalty_form)
    assert resp.http_response.status == 404


async def test_another_business(
    api_client: LoyaltyClient,
    business: BusinessUser,
    another_business: BusinessUser,
    loyalty_form: LoyaltyForm,
    update_loyalty_form: UpdateLoyaltyForm,
) -> None:
    business_token = business[2]
    another_business_token = another_business[2]

    api_client.authorize(business_token)

    resp_create = await api_client.create_loyalty(loyalty_form)

    assert resp_create.content is not None

    original_loyalty = (await api_client.read_loyalty(resp_create.content.loyalty_id)).content

    assert original_loyalty is not None

    api_client.authorize(another_business_token)

    resp_update = await api_client.update_loyalty(
        original_loyalty.loyalty_id,
        update_loyalty_form,
    )

    assert resp_update.http_response.status == 403


async def test_by_client(
    api_client: LoyaltyClient,
    business: BusinessUser,
    loyalty_form: LoyaltyForm,
    client_form: ClientForm,
    update_loyalty_form: UpdateLoyaltyForm,
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
    update_loyalty_form.name = "!!!"
    resp_update = await api_client.update_loyalty(resp_create.content.loyalty_id, update_loyalty_form)

    assert resp_update.http_response.status == 403
    assert resp_update.content is None
