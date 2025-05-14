from uuid import uuid4

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.application.payment.create import PaymentCreated
from tests.conftest import BusinessUser, ClientUser


async def test_ok(
    api_client: LoyaltyClient,
    payment: PaymentCreated,
    business: BusinessUser,
) -> None:
    api_client.authorize(business[2])
    content = (await api_client.read_payment(payment.payment_id)).except_status(200).unwrap()
    assert content.payment_id == payment.payment_id


async def test_by_another_business(
    api_client: LoyaltyClient,
    payment: PaymentCreated,
    another_business: BusinessUser,
) -> None:
    api_client.authorize(another_business[2])
    (await api_client.read_payment(payment.payment_id)).except_status(403)


async def test_by_client(
    api_client: LoyaltyClient,
    client: ClientUser,
) -> None:
    api_client.authorize(client[2])
    (await api_client.read_payment(uuid4())).except_status(403)


async def test_not_exist(
    api_client: LoyaltyClient,
    business: BusinessUser,
) -> None:
    api_client.authorize(business[2])
    (await api_client.read_payment(uuid4())).except_status(404)


async def test_unauthorized(
    api_client: LoyaltyClient,
) -> None:
    api_client.reset_authorization()
    (await api_client.read_payment(uuid4())).except_status(401)
