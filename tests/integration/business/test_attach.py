from pathlib import Path

from loyalty.adapters.api_client import LoyaltyClient
from tests.conftest import BusinessUser, ClientUser


async def test_ok(api_client: LoyaltyClient, business: BusinessUser, image_file: Path) -> None:
    src_business, _, token = business
    api_client.authorize(token)

    avatar_url = (await api_client.attach_business_avatar(image_file)).except_status(200).unwrap().avatar_url
    assert (await api_client.read_business(src_business.business_id)).unwrap().avatar_url == avatar_url


async def test_upload_twice(api_client: LoyaltyClient, business: BusinessUser, image_file: Path) -> None:
    src_business, _, token = business
    api_client.authorize(token)

    avatar_url_first = (await api_client.attach_business_avatar(image_file)).except_status(200).unwrap().avatar_url
    assert (await api_client.read_business(src_business.business_id)).unwrap().avatar_url == avatar_url_first

    avatar_url_second = (await api_client.attach_business_avatar(image_file)).except_status(200).unwrap().avatar_url
    assert (await api_client.read_business(src_business.business_id)).unwrap().avatar_url == avatar_url_second


async def test_text(api_client: LoyaltyClient, business: BusinessUser, text_file: Path) -> None:
    src_business, _, token = business
    api_client.authorize(token)

    (await api_client.attach_business_avatar(text_file)).except_status(422)
    assert (await api_client.read_business(src_business.business_id)).unwrap().avatar_url is None


async def test_without_ext(api_client: LoyaltyClient, business: BusinessUser, without_extension_file: Path) -> None:
    src_business, _, token = business
    api_client.authorize(token)

    (await api_client.attach_business_avatar(without_extension_file)).except_status(422)
    assert (await api_client.read_business(src_business.business_id)).unwrap().avatar_url is None


async def test_by_client(api_client: LoyaltyClient, client: ClientUser, image_file: Path) -> None:
    _, _, token = client
    api_client.authorize(token)

    (await api_client.attach_business_avatar(image_file)).except_status(403)

async def test_unauthorized(api_client: LoyaltyClient, image_file: Path) -> None:
    api_client.reset_authorization()

    (await api_client.attach_business_avatar(image_file)).except_status(401)
