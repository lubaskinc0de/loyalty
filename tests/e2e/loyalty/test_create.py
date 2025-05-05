from uuid import uuid4
import pytest

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.adapters.auth.provider import WebUserCredentials
from loyalty.application.client.create import ClientForm
from loyalty.application.loyalty.create import LoyaltyForm
from loyalty.domain.shared_types import Gender
from tests.e2e.conftest import BusinessUser, create_authorized_user, create_client


@pytest.mark.parametrize(
    "gender_value",
    [
        Gender.MALE,
        None,
    ],
)
async def test_ok(
    api_client: LoyaltyClient,
    business: BusinessUser,
    loyalty_form: LoyaltyForm,
    gender_value: Gender | None,
) -> None:
    token = business[2]
    api_client.authorize(token)

    loyalty_form.gender = gender_value

    resp_create = await api_client.create_loyalty(loyalty_form)

    assert resp_create.http_response.status == 200
    assert resp_create.content is not None

    resp_read = await api_client.read_loyalty(resp_create.content.loyalty_id)

    created_loyalty = resp_read.content
    assert created_loyalty is not None

    assert loyalty_form.name == created_loyalty.name
    assert loyalty_form.description == created_loyalty.description
    assert loyalty_form.starts_at == created_loyalty.starts_at
    assert loyalty_form.ends_at == created_loyalty.ends_at
    assert loyalty_form.money_per_bonus == created_loyalty.money_per_bonus
    assert loyalty_form.min_age == created_loyalty.min_age
    assert loyalty_form.max_age == created_loyalty.max_age
    assert loyalty_form.gender == created_loyalty.gender
    
async def test_fake_business(
    api_client: LoyaltyClient,
    loyalty_form: LoyaltyForm,
) -> None:
    fake_business_token = uuid4()
    
    api_client.authorize(fake_business_token)
    resp_create = await api_client.create_loyalty(loyalty_form)

    assert resp_create.http_response.status == 401


async def test_by_client(
    api_client: LoyaltyClient,
    loyalty_form: LoyaltyForm,
    client_form: ClientForm,
) -> None:
    client_user = await create_authorized_user(
        api_client,
        WebUserCredentials(
            username="someosskems",
            password="someeeeepasssswwww",  # noqa: S106
        ),
    )
    _, _, client_token = await create_client(api_client, client_form, client_user)
    api_client.authorize(client_token)

    resp_create = await api_client.create_loyalty(loyalty_form)

    assert resp_create.http_response.status == 403
    assert resp_create.content is None
