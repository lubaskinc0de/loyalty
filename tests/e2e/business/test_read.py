from uuid import uuid4

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.adapters.auth.provider import WebUserCredentials
from loyalty.application.client.create import ClientForm
from tests.e2e.conftest import BusinessUser, create_authorized_user, create_client


async def test_ok(
    api_client: LoyaltyClient,
    business: BusinessUser,
) -> None:
    src_business, _, token = business
    resp = await api_client.read_business(src_business.business_id, token)
    assert resp.http_response.status == 200
    assert resp.content is not None
    assert resp.content == src_business


async def test_not_found(
    api_client: LoyaltyClient,
    business: BusinessUser,
) -> None:
    _, _, token = business
    resp = await api_client.read_business(uuid4(), token)
    assert resp.http_response.status == 404


async def test_by_client(
    api_client: LoyaltyClient,
    business: BusinessUser,
    client_form: ClientForm,
) -> None:
    src_business, _, _ = business

    client_user = await create_authorized_user(
        api_client,
        WebUserCredentials(
            username="someosskems",
            password="someeeeepasssswwww",  # noqa: S106
        ),
    )
    _, _, token = await create_client(api_client, client_form, client_user)
    resp = await api_client.read_business(src_business.business_id, token)
    assert resp.http_response.status == 200
    assert resp.content is not None
    assert resp.content == src_business
