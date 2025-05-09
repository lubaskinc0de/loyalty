from uuid import uuid4

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.domain.entity.loyalty import Loyalty
from tests.conftest import BusinessUser, ClientUser


async def test_ok(
    api_client: LoyaltyClient,
    business: BusinessUser,
    loyalty: Loyalty,
) -> None:
    token = business[2]
    api_client.authorize(token)

    (await api_client.delete_loyalty(loyalty.loyalty_id)).except_status(204)
    (await api_client.read_loyalty(loyalty.loyalty_id)).except_status(404)


async def test_not_found(
    api_client: LoyaltyClient,
    business: BusinessUser,
) -> None:
    token = business[2]
    api_client.authorize(token)

    (await api_client.delete_loyalty(uuid4())).except_status(404)


async def test_another_business(
    api_client: LoyaltyClient,
    another_business: BusinessUser,
    loyalty: Loyalty,
) -> None:
    another_business_token = another_business[2]

    api_client.authorize(another_business_token)
    (await api_client.delete_loyalty(loyalty.loyalty_id)).except_status(403)


async def test_by_client(
    api_client: LoyaltyClient,
    loyalty: Loyalty,
    another_client: ClientUser,
) -> None:
    _, _, client_token = another_client

    api_client.authorize(client_token)
    (await api_client.delete_loyalty(loyalty.loyalty_id)).except_status(403)


async def test_fake_business(
    api_client: LoyaltyClient,
    loyalty: Loyalty,
) -> None:
    api_client.authorize(str(uuid4()))
    (await api_client.delete_loyalty(loyalty.loyalty_id)).except_status(401)


async def test_unauthorized(api_client: LoyaltyClient, loyalty: Loyalty) -> None:
    api_client.reset_authorization()
    (await api_client.delete_loyalty(loyalty.loyalty_id)).except_status(401)
