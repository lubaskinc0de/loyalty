import asyncio
from collections.abc import Coroutine
from decimal import ROUND_DOWN, Decimal
from typing import Any
from uuid import uuid4

import pytest

from loyalty.adapters.api_client import APIResponse, LoyaltyClient
from loyalty.adapters.api_models import LoyaltyId
from loyalty.application.loyalty.create import LoyaltyForm
from loyalty.application.membership.dto import MembershipData
from loyalty.application.payment.create import PaymentCreated
from tests.conftest import BusinessUser


@pytest.mark.parametrize(
    "loyalties_count",
    [
        1,
        2,
        3,
        4,
        5,
    ],
)
async def test_ok(
    api_client: LoyaltyClient,
    business: BusinessUser,
    membership: MembershipData,  # noqa: ARG001
    another_membership: MembershipData,  # noqa: ARG001
    payment: PaymentCreated,
    another_payment: PaymentCreated,
    loyalties_count: int,
    loyalty_form: LoyaltyForm,
) -> None:
    api_client.authorize(business[2])

    payments_amount = payment.payment_sum + another_payment.payment_sum
    waste_amount = payment.service_income + another_payment.service_income
    bonus_given = payment.bonus_income + another_payment.bonus_income

    loyalty_names = [uuid4().hex[:99] for _ in range(loyalties_count)]
    tasks: list[Coroutine[Any, Any, APIResponse[LoyaltyId]]] = []

    for name in loyalty_names:
        form = loyalty_form.model_copy(
            update={
                "name": name,
            },
        )
        tasks.append(api_client.create_loyalty(form))

    for each in await asyncio.gather(*tasks):
        each.except_status(200).unwrap()

    resp = (await api_client.read_business_stats()).except_status(200).unwrap()

    assert resp.bonus_given_amount == bonus_given.quantize(Decimal("0.01"), rounding=ROUND_DOWN)
    assert resp.loyalties_count == loyalties_count + 1
    assert resp.memberships_count == 2
    assert resp.payments_amount == payments_amount.quantize(Decimal("0.01"), rounding=ROUND_DOWN)
    assert resp.waste_amount == waste_amount.quantize(Decimal("0.01"), rounding=ROUND_DOWN)


async def test_zero(
    api_client: LoyaltyClient,
    business: BusinessUser,
) -> None:
    api_client.authorize(business[2])
    resp = (await api_client.read_business_stats()).except_status(200).unwrap()

    assert resp.bonus_given_amount == Decimal(0)
    assert resp.loyalties_count == 0
    assert resp.memberships_count == 0
    assert resp.payments_amount == Decimal(0)
    assert resp.waste_amount == Decimal(0)


async def test_unauthorized(
    api_client: LoyaltyClient,
) -> None:
    api_client.reset_authorization()
    (await api_client.read_business_stats()).except_status(401)
