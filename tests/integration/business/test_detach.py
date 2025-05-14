from pathlib import Path

from loyalty.adapters.api_client import LoyaltyClient
from tests.conftest import BusinessUser, ClientUser


async def test_ok(api_client: LoyaltyClient, business: BusinessUser, image_file: Path) -> None:
    src_business, _, token = business
    api_client.authorize(token)

    (await api_client.attach_business_avatar(image_file)).except_status(200)
    assert (await api_client.read_business(src_business.business_id)).unwrap().avatar_url is not None

    (await api_client.detach_business_avatar()).except_status(204)
    assert (await api_client.read_business(src_business.business_id)).unwrap().avatar_url is None


async def test_detach_empty(api_client: LoyaltyClient, business: BusinessUser) -> None:
    _, _, token = business
    api_client.authorize(token)

    (await api_client.detach_business_avatar()).except_status(204)


async def test_by_client(api_client: LoyaltyClient, client: ClientUser) -> None:
    _, _, token = client
    api_client.authorize(token)

    (await api_client.detach_business_avatar()).except_status(403)


async def test_unauthorized(api_client: LoyaltyClient) -> None:
    api_client.reset_authorization()
    (await api_client.detach_business_avatar()).except_status(401)
