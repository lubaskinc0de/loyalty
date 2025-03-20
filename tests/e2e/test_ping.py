from tests.e2e.api_client import TestAPIClient
from tests.e2e.status import OK


async def test_ok(client: TestAPIClient) -> None:
    resp = await client.ping()
    assert resp.http_response.status == OK
    assert resp.content == "pong"
