import asyncio
import random
from collections.abc import Coroutine
from decimal import ROUND_DOWN, Decimal
from typing import Any
from uuid import uuid4

import pytest

from loyalty.adapters.api_client import APIResponse, LoyaltyClient
from loyalty.adapters.api_models import LoyaltyId, MembershipId
from loyalty.application.data_model.business_branch import BusinessBranchData
from loyalty.application.loyalty.create import LoyaltyForm
from loyalty.application.membership.create import MembershipForm
from loyalty.application.payment.create import PaymentCreated, PaymentForm
from tests.conftest import BusinessUser, ClientUser


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
    client: ClientUser,
    loyalties_count: int,
    loyalty_form: LoyaltyForm,
    branch: BusinessBranchData,
) -> None:
    client_obj, _, client_token = client

    payments_amount = Decimal(0)
    waste_amount = Decimal(0)
    bonus_given = Decimal(0)

    loyalty_names = [uuid4().hex[:99] for _ in range(loyalties_count)]
    tasks_loyalty: list[Coroutine[Any, Any, APIResponse[LoyaltyId]]] = []
    tasks_membership: list[Coroutine[Any, Any, APIResponse[MembershipId]]] = []
    tasks_payment: list[Coroutine[Any, Any, APIResponse[PaymentCreated]]] = []

    for name in loyalty_names:
        form = loyalty_form.model_copy(
            update={
                "name": name,
            },
        )
        tasks_loyalty.append(api_client.create_loyalty(form))

    api_client.authorize(business[2])
    for loyalty_req in await asyncio.gather(*tasks_loyalty):
        loyalty_id = loyalty_req.except_status(200).unwrap()
        tasks_membership.append(
            api_client.create_membership(
                MembershipForm(
                    loyalty_id=loyalty_id.loyalty_id,
                ),
            ),
        )
    api_client.authorize(client_token)
    for memberhip_req in await asyncio.gather(*tasks_membership):
        membership_id = memberhip_req.except_status(200).unwrap().membership_id
        payment_sum = Decimal(random.randint(100, 1000))  # noqa: S311
        tasks_payment.append(
            api_client.create_payment(
                PaymentForm(
                    payment_sum=payment_sum,
                    membership_id=membership_id,
                    business_branch_id=branch.business_branch_id,
                    client_id=client_obj.client_id,
                ),
            ),
        )
    api_client.authorize(business[2])
    for payment_req in await asyncio.gather(*tasks_payment):
        payment_info = payment_req.except_status(200).unwrap()
        payments_amount += payment_info.payment_sum
        waste_amount += payment_info.service_income
        bonus_given += payment_info.bonus_income

    resp = (await api_client.read_business_stats()).except_status(200).unwrap()

    assert resp.bonus_given_amount == bonus_given.quantize(Decimal("0.01"), rounding=ROUND_DOWN)
    assert resp.loyalties_count == loyalties_count
    assert resp.memberships_count == len(tasks_membership)
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
