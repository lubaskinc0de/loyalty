from uuid import uuid4

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.application.loyalty.create import LoyaltyForm
from tests.e2e.conftest import BusinessUser


async def test_ok(
    api_client: LoyaltyClient,
    business: BusinessUser,
    loyalty_form: LoyaltyForm,
) -> None:
    token = business[2]
    api_client.authorize(token)

    resp_create = await api_client.create_loyalty(loyalty_form)

    assert resp_create.content is not None

    loyalty = (await api_client.read_loyalty(resp_create.content.loyalty_id)).content

    assert loyalty is not None

    resp_delete = await api_client.delete_loyalty(loyalty.loyalty_id)

    resp_read = await api_client.read_loyalty(loyalty.loyalty_id)

    assert resp_delete.http_response.status == 204
    assert resp_read.http_response.status == 404


async def test_not_found(
    api_client: LoyaltyClient,
    business: BusinessUser,
) -> None:
    token = business[2]
    api_client.authorize(token)

    resp = await api_client.delete_loyalty(uuid4())
    assert resp.http_response.status == 404


async def test_another_business(
    api_client: LoyaltyClient,
    business: BusinessUser,
    another_business: BusinessUser,
    loyalty_form: LoyaltyForm,
) -> None:
    token = business[2]
    another_business_token = another_business[2]
    api_client.authorize(token)

    resp_create = await api_client.create_loyalty(loyalty_form)

    assert resp_create.content is not None

    loyalty = (await api_client.read_loyalty(resp_create.content.loyalty_id)).content

    assert loyalty is not None

    api_client.authorize(another_business_token)

    resp_delete = await api_client.delete_loyalty(loyalty.loyalty_id)
    assert resp_delete.http_response.status == 403


async def test_fake_business(
    api_client: LoyaltyClient,
    business: BusinessUser,
    loyalty_form: LoyaltyForm,
) -> None:
    token = business[2]
    fake_business_token = uuid4()
    api_client.authorize(token)

    resp_create = await api_client.create_loyalty(loyalty_form)

    assert resp_create.content is not None

    loyalty = (await api_client.read_loyalty(resp_create.content.loyalty_id)).content

    assert loyalty is not None

    api_client.authorize(fake_business_token)

    resp_delete = await api_client.delete_loyalty(loyalty.loyalty_id)
    assert resp_delete.http_response.status == 401
