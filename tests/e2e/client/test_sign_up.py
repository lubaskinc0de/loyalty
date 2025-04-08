from loyalty.presentation.web.controller.sign_up_client import ClientWebSignUpForm
from tests.e2e.api_client import TestAPIClient


async def test_ok(api_client: TestAPIClient, valid_client_signup_form: ClientWebSignUpForm) -> None:
    resp = await api_client.sign_up_client(valid_client_signup_form)

    assert resp.http_response.status == 200
    assert resp.content is not None
    assert resp.content.client is not None

    assert resp.content.client.age == valid_client_signup_form.client_data.age
    assert resp.content.client.full_name == valid_client_signup_form.client_data.full_name
    assert resp.content.client.gender == valid_client_signup_form.client_data.gender
    assert resp.content.client.phone == str(valid_client_signup_form.client_data.phone)
    assert (
        resp.content.client.location
        == f"POINT({float(valid_client_signup_form.client_data.lon)} {float(valid_client_signup_form.client_data.lat)})"
    )


async def test_already_exists(api_client: TestAPIClient, valid_client_signup_form: ClientWebSignUpForm) -> None:
    resp = await api_client.sign_up_client(valid_client_signup_form)
    assert resp.http_response.status == 200

    resp_two = await api_client.sign_up_client(valid_client_signup_form)
    assert resp_two.http_response.status == 409
