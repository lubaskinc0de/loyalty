from loyalty.adapters.api_client import LoyaltyClient
from tests.e2e.conftest import AuthorizedUser, BusinessUser, ClientUser


async def test_ok(
    api_client: LoyaltyClient,
    authorized_user: AuthorizedUser,
) -> None:
    user, token = authorized_user
    api_client.authorize(token)

    resp = await api_client.read_user()

    assert resp.http_response.status == 200
    assert resp.content is not None
    assert resp.content == user


async def test_ok_with_roles(
    api_client: LoyaltyClient,
    authorized_user: AuthorizedUser,
    client: ClientUser,
    business: BusinessUser,
) -> None:
    user, token = authorized_user
    api_client.authorize(token)

    resp = await api_client.read_user()

    assert resp.http_response.status == 200
    assert resp.content is not None
    assert resp.content.user_id == user.user_id
    assert resp.content.business == business[0]
    assert resp.content.client == client[0]
