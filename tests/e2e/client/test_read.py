from loyalty.adapters.api_client import LoyaltyClient
from tests.e2e.conftest import ClientUser


async def test_ok(
    api_client: LoyaltyClient,
    client: ClientUser,
) -> None:
    src_client, _, token = client
    resp = await api_client.read_client(token)
    assert resp.http_response.status == 200
    assert resp.content is not None
    assert resp.content == src_client
