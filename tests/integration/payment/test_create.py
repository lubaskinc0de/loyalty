from decimal import Decimal
from uuid import uuid4

import pytest
from pydantic import ValidationError

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.application.payment.create import PaymentForm
from loyalty.domain.entity.membership import LoyaltyMembership
from loyalty.domain.service.payment import SERVICE_INCOME_PERCENT
from tests.conftest import BusinessUser, ClientUser


async def test_ok(api_client: LoyaltyClient, membership: LoyaltyMembership, client: ClientUser) -> None:
    client_obj, _, token = client
    payment_sum = Decimal("100.05")
    api_client.authorize(token)
    form = PaymentForm(
        payment_sum=payment_sum,
        membership_id=membership.membership_id,
    )

    payment = (await api_client.create_payment(form)).except_status(200).unwrap()

    assert payment.client_id == client_obj.client_id
    assert payment.bonus_income == payment_sum // membership.loyalty.money_per_bonus
    assert payment.service_income == payment_sum * SERVICE_INCOME_PERCENT


async def test_negative_payment_summ(membership: LoyaltyMembership) -> None:
    with pytest.raises(ValidationError):
        PaymentForm(
            payment_sum=Decimal("-100.05"),
            membership_id=membership.membership_id,
        )


async def test_by_other_client(
    api_client: LoyaltyClient,
    membership: LoyaltyMembership,
    another_client: ClientUser,
) -> None:
    _, _, token = another_client
    api_client.authorize(token)
    form = PaymentForm(
        payment_sum=Decimal("100.05"),
        membership_id=membership.membership_id,
    )

    (await api_client.create_payment(form)).except_status(403)


async def test_fake_membership(api_client: LoyaltyClient, client: ClientUser) -> None:
    _, _, token = client
    api_client.authorize(token)
    form = PaymentForm(
        payment_sum=Decimal("100.05"),
        membership_id=uuid4(),
    )

    (await api_client.create_payment(form)).except_status(404)


async def test_as_business(api_client: LoyaltyClient, business: BusinessUser) -> None:
    _, _, token = business
    api_client.authorize(token)
    form = PaymentForm(
        payment_sum=Decimal("100.05"),
        membership_id=uuid4(),
    )

    (await api_client.create_payment(form)).except_status(403)


async def test_unauthorized(api_client: LoyaltyClient, membership: LoyaltyMembership) -> None:
    api_client.reset_authorization()
    form = PaymentForm(
        payment_sum=Decimal("100.05"),
        membership_id=membership.membership_id,
    )

    (await api_client.create_payment(form)).except_status(401)
