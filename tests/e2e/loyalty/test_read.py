from uuid import uuid4

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.adapters.auth.provider import WebUserCredentials
from loyalty.application.client.create import ClientForm
from loyalty.application.data_model.loyalty import LoyaltyForm
from tests.e2e.conftest import BusinessUser, create_authorized_user, create_client


async def test_ok(
    api_client: LoyaltyClient,
    business: BusinessUser,
    loyalty_form: LoyaltyForm,
) -> None:
    token = business[2]
    resp_create = await api_client.create_loyalty(loyalty_form, token)

    assert resp_create.content is not None

    resp = await api_client.read_loyalty(
        resp_create.content.loyalty_id,
        token,
    )

    assert resp.http_response.status == 200
    assert resp.content is not None


async def test_not_found(
    api_client: LoyaltyClient,
    business: BusinessUser,
) -> None:
    token = business[2]
    resp = await api_client.read_loyalty(uuid4(), token)
    assert resp.http_response.status == 404


async def test_by_client(
    api_client: LoyaltyClient,
    business: BusinessUser,
    client_form: ClientForm,
    loyalty_form: LoyaltyForm,
) -> None:
    business_token = business[2]

    client_user = await create_authorized_user(
        api_client,
        WebUserCredentials(
            username="someosskems",
            password="someeeeepasssswwww",  # noqa: S106
        ),
    )
    _, _, token = await create_client(api_client, client_form, client_user)

    resp_create = await api_client.create_loyalty(
        loyalty_form,
        business_token,
    )

    assert resp_create.content is not None

    loyalty = (
        await api_client.read_loyalty(
            resp_create.content.loyalty_id,
            token,
        )
    ).content

    assert loyalty is not None

    resp = await api_client.read_loyalty(
        loyalty.loyalty_id,
        token,
    )

    assert resp.http_response.status == 200
    assert resp.content is not None
    assert resp.content == loyalty
