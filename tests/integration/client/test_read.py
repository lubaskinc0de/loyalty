from loyalty.adapters.api_client import LoyaltyClient
from tests.conftest import ClientUser


async def test_ok(
    api_client: LoyaltyClient,
    client: ClientUser,
) -> None:
    src_client, _, token = client
    api_client.authorize(token)

    resp = await api_client.read_client()
    assert resp.http_response.status == 200
    assert resp.content is not None
    assert resp.content == src_client
