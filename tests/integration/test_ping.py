from loyalty.adapters.api_client import LoyaltyClient


async def test_ok(api_client: LoyaltyClient) -> None:
    resp = await api_client.ping()
    assert resp.http_response.status == 200
    assert resp.content is not None
    assert resp.content.ping == "pong"
