from uuid import uuid4

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.application.loyalty.dto import LoyaltyData
from tests.conftest import BusinessUser, ClientUser


async def test_ok(
    api_client: LoyaltyClient,
    business: BusinessUser,
    loyalty: LoyaltyData,
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
    loyalty: LoyaltyData,
) -> None:
    another_business_token = another_business[2]

    api_client.authorize(another_business_token)
    (await api_client.delete_loyalty(loyalty.loyalty_id)).except_status(403)


async def test_by_client(
    api_client: LoyaltyClient,
    loyalty: LoyaltyData,
    another_client: ClientUser,
) -> None:
    _, _, client_token = another_client

    api_client.authorize(client_token)
    (await api_client.delete_loyalty(loyalty.loyalty_id)).except_status(403)


async def test_fake_business(
    api_client: LoyaltyClient,
    loyalty: LoyaltyData,
) -> None:
    api_client.authorize(str(uuid4()))
    (await api_client.delete_loyalty(loyalty.loyalty_id)).except_status(401)


async def test_unauthorized(api_client: LoyaltyClient, loyalty: LoyaltyData) -> None:
    api_client.reset_authorization()
    (await api_client.delete_loyalty(loyalty.loyalty_id)).except_status(401)
