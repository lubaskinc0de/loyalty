from decimal import Decimal

import pytest

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.application.data_model.business_branch import BusinessBranchData
from loyalty.application.membership.dto import MembershipData
from loyalty.application.payment.create import PaymentForm
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
    client: ClientUser,
    business: BusinessUser,
    branch: BusinessBranchData,
    bonus_balance: Decimal,
    purchase_amount: Decimal,
) -> None:
    client_obj, _, client_token = client
    _, _, token = business
    payment_sum = purchase_amount
    api_client.authorize(token)
    max_discount = purchase_amount * MAX_DISCOUNT
    potential_discount = bonus_balance * membership.loyalty.money_for_bonus
    actual_discount = min(potential_discount, max_discount)
    expected_used_bonuses = actual_discount / membership.loyalty.money_for_bonus

    form = PaymentForm(
        payment_sum=payment_sum,
        membership_id=membership.membership_id,
        business_branch_id=branch.business_branch_id,
        client_id=client_obj.client_id,
        apply_discount=True,
    )

    payment = (await api_client.create_payment(form)).except_status(200).unwrap()
    assert payment.bonus_spent == expected_used_bonuses
    assert payment.discount_sum == actual_discount

    api_client.authorize(client_token)
    new_bonus_balance = (await api_client.read_bonuses(membership.membership_id)).unwrap()

    expected_balance = bonus_balance - expected_used_bonuses + payment.bonus_income
    assert new_bonus_balance.balance == round(expected_balance, 2)


async def test_with_zero_balance(
    api_client: LoyaltyClient,
    membership: MembershipData,
    client: ClientUser,
    business: BusinessUser,
    branch: BusinessBranchData,
) -> None:
    client_obj, _, client_token = client
    _, _, token = business
    purchase_amount = Decimal("2000")
    payment_sum = purchase_amount
    api_client.authorize(token)

    form = PaymentForm(
        payment_sum=payment_sum,
        membership_id=membership.membership_id,
        business_branch_id=branch.business_branch_id,
        client_id=client_obj.client_id,
        apply_discount=True,
    )

    payment = (await api_client.create_payment(form)).except_status(200).unwrap()
    assert payment.bonus_spent == 0
    assert payment.discount_sum == 0

    api_client.authorize(client_token)
    new_bonus_balance = (await api_client.read_bonuses(membership.membership_id)).unwrap()
    assert new_bonus_balance.balance == payment.bonus_income
