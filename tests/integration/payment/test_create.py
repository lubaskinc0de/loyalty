from decimal import Decimal
from uuid import uuid4

import pytest
from pydantic import ValidationError

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.application.data_model.business_branch import BusinessBranchData
from loyalty.application.membership.dto import MembershipData
from loyalty.application.payment.create import PaymentForm
from loyalty.domain.service.payment import calc_bonus_income, calc_service_income
from tests.conftest import BusinessUser, ClientUser


async def test_ok(
    api_client: LoyaltyClient,
    membership: MembershipData,
    client: ClientUser,
    business: BusinessUser,
    branch: BusinessBranchData,
) -> None:
    client_obj, _, client_token = client
    business_obj, _, token = business
    payment_sum = Decimal("100.05")
    api_client.authorize(token)
    form = PaymentForm(
        payment_sum=payment_sum,
        membership_id=membership.membership_id,
        business_branch_id=branch.business_branch_id,
        client_id=client_obj.client_id,
    )

    payment = (await api_client.create_payment(form)).except_status(200).unwrap()

    assert payment.client_id == client_obj.client_id
    assert payment.bonus_income == calc_bonus_income(payment_sum, membership.loyalty.money_per_bonus, Decimal(0))
    assert payment.service_income == calc_service_income(payment_sum)
    assert payment.business_id == business_obj.business_id
    assert payment.bonus_spent == Decimal(0)
    assert payment.discount_sum == Decimal(0)
    assert payment.payment_sum == payment_sum

    api_client.authorize(client_token)
    bonus_balance = (await api_client.read_bonuses(membership.membership_id)).unwrap()
    assert bonus_balance.balance == payment.bonus_income

    payment2 = (await api_client.create_payment(form)).except_status(200).unwrap()
    assert payment2.bonus_income > payment.bonus_income


async def test_by_client(
    api_client: LoyaltyClient,
    client: ClientUser,
) -> None:
    client_obj, _, token = client
    payment_sum = Decimal("100.05")
    api_client.authorize(token)
    form = PaymentForm(
        payment_sum=payment_sum,
        membership_id=uuid4(),
        business_branch_id=uuid4(),
        client_id=client_obj.client_id,
    )

    (await api_client.create_payment(form)).except_status(403)


async def test_another_branch(
    api_client: LoyaltyClient,
    membership: MembershipData,
    client: ClientUser,
    business: BusinessUser,
    another_branch: BusinessBranchData,
) -> None:
    client_obj, _, _ = client
    _, _, token = business
    payment_sum = Decimal("100.05")
    api_client.authorize(token)
    form = PaymentForm(
        payment_sum=payment_sum,
        membership_id=membership.membership_id,
        business_branch_id=another_branch.business_branch_id,
        client_id=client_obj.client_id,
    )

    (await api_client.create_payment(form)).except_status(403)


async def test_another_business(
    api_client: LoyaltyClient,
    membership: MembershipData,
    client: ClientUser,
    another_business: BusinessUser,
    branch: BusinessBranchData,
) -> None:
    client_obj, _, _ = client
    _, _, token = another_business
    payment_sum = Decimal("100.05")
    api_client.authorize(token)
    form = PaymentForm(
        payment_sum=payment_sum,
        membership_id=membership.membership_id,
        business_branch_id=branch.business_branch_id,
        client_id=client_obj.client_id,
    )

    (await api_client.create_payment(form)).except_status(403)


async def test_another_client(
    api_client: LoyaltyClient,
    membership: MembershipData,
    another_client: ClientUser,
    business: BusinessUser,
    branch: BusinessBranchData,
) -> None:
    client_obj, _, _ = another_client
    _, _, token = business
    payment_sum = Decimal("100.05")
    api_client.authorize(token)
    form = PaymentForm(
        payment_sum=payment_sum,
        membership_id=membership.membership_id,
        business_branch_id=branch.business_branch_id,
        client_id=client_obj.client_id,
    )

    (await api_client.create_payment(form)).except_status(403)


async def test_negative_summ() -> None:
    with pytest.raises(ValidationError):
        PaymentForm(
            payment_sum=Decimal("-1"),
            membership_id=uuid4(),
            business_branch_id=uuid4(),
            client_id=uuid4(),
        )


async def test_fake_client(
    api_client: LoyaltyClient,
    membership: MembershipData,
    business: BusinessUser,
    branch: BusinessBranchData,
) -> None:
    (
        _,
        _,
        token,
    ) = business
    payment_sum = Decimal("100.05")
    api_client.authorize(token)
    form = PaymentForm(
        payment_sum=payment_sum,
        membership_id=membership.membership_id,
        business_branch_id=branch.business_branch_id,
        client_id=uuid4(),
    )

    (await api_client.create_payment(form)).except_status(404)


async def test_fake_membership(
    api_client: LoyaltyClient,
    client: ClientUser,
    business: BusinessUser,
    branch: BusinessBranchData,
) -> None:
    client_obj, _, _ = client
    _, _, token = business
    payment_sum = Decimal("100.05")
    api_client.authorize(token)
    form = PaymentForm(
        payment_sum=payment_sum,
        membership_id=uuid4(),
        business_branch_id=branch.business_branch_id,
        client_id=client_obj.client_id,
    )

    (await api_client.create_payment(form)).except_status(404)


async def test_fake_branch(
    api_client: LoyaltyClient,
    membership: MembershipData,
    client: ClientUser,
    business: BusinessUser,
) -> None:
    client_obj, _, _ = client
    _, _, token = business
    payment_sum = Decimal("100.05")
    api_client.authorize(token)
    form = PaymentForm(
        payment_sum=payment_sum,
        membership_id=membership.membership_id,
        business_branch_id=uuid4(),
        client_id=client_obj.client_id,
    )

    (await api_client.create_payment(form)).except_status(404)


async def test_unauthorized(
    api_client: LoyaltyClient,
) -> None:
    payment_sum = Decimal("100.05")
    api_client.reset_authorization()
    form = PaymentForm(
        payment_sum=payment_sum,
        membership_id=uuid4(),
        business_branch_id=uuid4(),
        client_id=uuid4(),
    )

    (await api_client.create_payment(form)).except_status(401)
