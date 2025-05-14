from decimal import Decimal
from uuid import uuid4

import pytest

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.application.membership.dto import MembershipData
from loyalty.domain.entity.loyalty import MAX_DISCOUNT
from tests.conftest import BusinessUser, ClientUser


@pytest.mark.parametrize(
    "purchase_amount",
    [
        Decimal("20000"),
        Decimal("2000.78"),
        Decimal("0.01"),
        Decimal("10000000"),
        Decimal("1"),
    ],
)
async def test_ok(
    api_client: LoyaltyClient,
    membership: MembershipData,
    business: BusinessUser,
    bonus_balance: Decimal,
    purchase_amount: Decimal,
) -> None:
    api_client.authorize(business[2])
    max_discount = purchase_amount * MAX_DISCOUNT
    potential_discount = bonus_balance * membership.loyalty.money_for_bonus
    actual_discount = min(potential_discount, max_discount)

    resp = await api_client.calc_discount(membership.membership_id, purchase_amount)
    resp.except_status(200)

    expected_used_bonuses = actual_discount / membership.loyalty.money_for_bonus
    expected_amount = purchase_amount - actual_discount
    content = resp.unwrap()
    assert content.bonus_spent == expected_used_bonuses
    assert content.new_amount == expected_amount


async def test_without_balance(
    api_client: LoyaltyClient,
    membership: MembershipData,
    business: BusinessUser,
) -> None:
    api_client.authorize(business[2])
    purchase_amount = Decimal("20000")

    resp = await api_client.calc_discount(membership.membership_id, purchase_amount)
    resp.except_status(200)

    content = resp.unwrap()
    assert content.bonus_spent == 0
    assert content.new_amount == purchase_amount


async def test_zero_purchase_amount(
    api_client: LoyaltyClient,
    membership: MembershipData,
    business: BusinessUser,
) -> None:
    api_client.authorize(business[2])
    purchase_amount = Decimal("0")

    resp = await api_client.calc_discount(membership.membership_id, purchase_amount)
    resp.except_status(422)


async def test_incorrect_purchase_amount(
    api_client: LoyaltyClient,
    membership: MembershipData,
    business: BusinessUser,
) -> None:
    api_client.authorize(business[2])
    purchase_amount = [1, 2, 3]

    resp = await api_client.calc_discount(membership.membership_id, purchase_amount)  # type: ignore
    resp.except_status(422)


async def test_incorrect_membership_id(
    api_client: LoyaltyClient,
    business: BusinessUser,
) -> None:
    api_client.authorize(business[2])
    resp = await api_client.calc_discount([1, 2, 3], Decimal("100"))  # type: ignore
    resp.except_status(422)


async def test_fake_membership(
    api_client: LoyaltyClient,
    business: BusinessUser,
) -> None:
    api_client.authorize(business[2])
    resp = await api_client.calc_discount(uuid4(), Decimal(100))
    resp.except_status(404)


async def test_by_client(
    api_client: LoyaltyClient,
    client: ClientUser,
) -> None:
    api_client.authorize(client[2])
    resp = await api_client.calc_discount(uuid4(), Decimal("100"))
    resp.except_status(403)


async def test_unauthorized(
    api_client: LoyaltyClient,
) -> None:
    api_client.reset_authorization()
    resp = await api_client.calc_discount(uuid4(), Decimal("422"))
    resp.except_status(401)
