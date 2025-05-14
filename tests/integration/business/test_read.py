from uuid import uuid4

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.adapters.auth.provider import WebUserCredentials
from loyalty.application.client.create import ClientForm
from tests.conftest import BusinessUser, create_authorized_user, create_client


async def test_ok(
    api_client: LoyaltyClient,
    business: BusinessUser,
) -> None:
    src_business, _, token = business
    api_client.authorize(token)

    resp = await api_client.read_business(src_business.business_id)
    assert resp.http_response.status == 200
    assert resp.content is not None
    assert resp.content == src_business


async def test_not_found(
    api_client: LoyaltyClient,
    business: BusinessUser,
) -> None:
    token = business[2]
    api_client.authorize(token)

    resp = await api_client.read_business(uuid4())
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
    _, _, client_token = await create_client(api_client, client_form, client_user)

    api_client.authorize(client_token)
    resp = await api_client.read_business(src_business.business_id)

    assert resp.http_response.status == 200
    assert resp.content is not None
    assert resp.content == src_business


async def test_many_anauthorized(
    api_client: LoyaltyClient,
    business: BusinessUser,
    another_business: BusinessUser,
) -> None:
    src_business = business[0]
    src_another_business = another_business[0]

    read_businesses = (await api_client.read_businesses()).except_status(200).unwrap()

    assert tuple(read_businesses.businesses) == (src_business, src_another_business)
