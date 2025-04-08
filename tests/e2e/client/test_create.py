from loyalty.application.client.create import ClientForm
from tests.e2e.api_client import TestAPIClient
from tests.e2e.conftest import AuthorizedUser, ClientUser


async def test_ok(api_client: TestAPIClient, client_form: ClientForm, authorized_user: AuthorizedUser) -> None:
    resp = await api_client.create_client(client_form, authorized_user[1])

    assert resp.http_response.status == 200
    assert resp.content is not None

    assert resp.content.age == client_form.age
    assert resp.content.full_name == client_form.full_name
    assert resp.content.gender == client_form.gender
    assert resp.content.phone == str(client_form.phone)
    assert resp.content.location == f"POINT({float(client_form.lon)} {float(client_form.lat)})"


async def test_already_exists(
    api_client: TestAPIClient,
    client: ClientUser,
    client_form: ClientForm,
) -> None:
    _, _, token = client
    resp = await api_client.create_client(client_form, token)
    assert resp.http_response.status == 409
