from loyalty.adapters.api_client import LoyaltyClient
from loyalty.adapters.auth.provider import WebUserCredentials


async def test_ok(api_client: LoyaltyClient, auth_data: WebUserCredentials) -> None:
    r = await api_client.web_sign_up(auth_data)
    assert r.http_response.status == 200

    assert r.content is not None
    assert not r.content.available_roles


async def test_twice(api_client: LoyaltyClient, auth_data: WebUserCredentials) -> None:
    r = await api_client.web_sign_up(auth_data)
    assert r.http_response.status == 200

    r2 = await api_client.web_sign_up(auth_data)
    assert r2.http_response.status == 409
