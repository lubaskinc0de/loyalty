import asyncio

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.application.loyalty.create import LoyaltyForm
from tests.conftest import BusinessUser, ClientUser


async def test_ok(
    api_client: LoyaltyClient,
    business: BusinessUser,
    client: ClientUser,
    loyalty_form: LoyaltyForm,
) -> None: ...
