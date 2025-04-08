from loyalty.adapters.auth.provider import WebUserCredentials
from tests.e2e.api_client import TestAPIClient


async def test_ok(api_client: TestAPIClient, auth_data: WebUserCredentials) -> None:
    r = await api_client.web_sign_up(auth_data)
    assert r.http_response.status == 200

    assert r.content is not None
    assert not r.content.available_roles


async def test_twice(api_client: TestAPIClient, auth_data: WebUserCredentials) -> None:
    r = await api_client.web_sign_up(auth_data)
    assert r.http_response.status == 200

    r2 = await api_client.web_sign_up(auth_data)
    assert r2.http_response.status == 409
