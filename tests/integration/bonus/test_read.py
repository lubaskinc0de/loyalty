from decimal import Decimal
from uuid import uuid4

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.application.membership.dto import MembershipData
from tests.conftest import BusinessUser, ClientUser


async def test_ok(
    api_client: LoyaltyClient,
    membership: MembershipData,
    client: ClientUser,
    bonus_balance: Decimal,
) -> None:
    api_client.authorize(client[2])
    res = (await api_client.read_bonuses(membership.membership_id)).except_status(200).unwrap()
    assert res.balance == bonus_balance


async def test_zero(
    api_client: LoyaltyClient,
    membership: MembershipData,
    client: ClientUser,
) -> None:
    api_client.authorize(client[2])

    res = (await api_client.read_bonuses(membership.membership_id)).except_status(200).unwrap()

    assert res.balance == Decimal("0.000")


async def test_another_client(
    api_client: LoyaltyClient,
    membership: MembershipData,
    another_client: ClientUser,
) -> None:
    api_client.authorize(another_client[2])

    (await api_client.read_bonuses(membership.membership_id)).except_status(403)


async def test_fake_membership(
    api_client: LoyaltyClient,
    client: ClientUser,
) -> None:
    api_client.authorize(client[2])

    (await api_client.read_bonuses(uuid4())).except_status(404)


async def test_as_business(
    api_client: LoyaltyClient,
    business: BusinessUser,
) -> None:
    api_client.authorize(business[2])

    (await api_client.read_bonuses(uuid4())).except_status(403)


async def test_unauthorized(
    api_client: LoyaltyClient,
) -> None:
    api_client.reset_authorization()

    (await api_client.read_bonuses(uuid4())).except_status(401)
