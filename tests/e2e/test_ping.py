from tests.e2e.api_client import TestAPIClient
from tests.e2e.status import OK


async def test_ok(api_client: TestAPIClient) -> None:
    resp = await api_client.ping()
    assert resp.http_response.status == OK
    assert resp.content is not None
    assert resp.content.ping == "pong"
