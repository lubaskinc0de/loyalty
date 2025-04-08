from loyalty.adapters.api_client import LoyaltyClient
from loyalty.application.client.create import ClientForm
from tests.e2e.conftest import AuthorizedUser, ClientUser


async def test_ok(api_client: LoyaltyClient, client_form: ClientForm, authorized_user: AuthorizedUser) -> None:
    resp = await api_client.create_client(client_form, authorized_user[1])
    assert resp.http_response.status == 204


async def test_already_exists(
    api_client: LoyaltyClient,
    client: ClientUser,
    client_form: ClientForm,
) -> None:
    _, _, token = client
    resp = await api_client.create_client(client_form, token)
    assert resp.http_response.status == 409
