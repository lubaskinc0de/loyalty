import asyncio
from collections.abc import Coroutine
from decimal import Decimal
from typing import Any
from uuid import uuid4

from loyalty.adapters.api_client import APIResponse, LoyaltyClient
from loyalty.application.data_model.business_branch import BusinessBranchData
from loyalty.application.membership.dto import MembershipData
from loyalty.application.payment.create import PaymentCreated, PaymentForm
from tests.conftest import BusinessUser, ClientUser


async def test_ok(
    api_client: LoyaltyClient,
    membership: MembershipData,
    client: ClientUser,
    business: BusinessUser,
    branch: BusinessBranchData,
) -> None:
    api_client.authorize(business[2])
    payments = [Decimal(x) for x in ["100.67", "254.87", "1000.78"]]
    expected_summ = Decimal("0.0")

    tasks: list[Coroutine[Any, Any, APIResponse[PaymentCreated]]] = []
    for summ in payments:
        payment_form = PaymentForm(
            payment_sum=summ,
            membership_id=membership.membership_id,
            business_branch_id=branch.business_branch_id,
            client_id=client[0].client_id,
        )
        tasks.append(api_client.create_payment(payment_form))

    for result in await asyncio.gather(*tasks):
        expected_summ += result.unwrap().bonus_income

    api_client.authorize(client[2])
    res = (await api_client.read_bonuses(membership.membership_id)).except_status(200).unwrap()
    assert res.balance == expected_summ


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
