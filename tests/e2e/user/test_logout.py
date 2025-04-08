from loyalty.adapters.api_client import LoyaltyClient
from tests.e2e.conftest import AuthorizedUser


async def test_ok(
    api_client: LoyaltyClient,
    authorized_user: AuthorizedUser,
) -> None:
    resp = await api_client.logout(authorized_user[1])
    assert resp.http_response.status == 204

    resp_info = await api_client.read_user(authorized_user[1])
    assert resp_info.http_response.status == 401
