from loyalty.adapters.api_client import LoyaltyClient
from tests.conftest import AuthorizedUser


async def test_ok(
    api_client: LoyaltyClient,
    authorized_user: AuthorizedUser,
) -> None:
    token = authorized_user[1]
    api_client.authorize(token)

    resp = await api_client.logout()
    assert resp.http_response.status == 204

    resp_info = await api_client.read_user()
    assert resp_info.http_response.status == 401
