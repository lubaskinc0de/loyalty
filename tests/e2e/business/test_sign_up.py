from loyalty.application.exceptions.business import BusinessAlreadyExistsError
from loyalty.application.exceptions.user import UserAlreadyExistsError
from loyalty.presentation.web.controller.sign_up_business import BusinessWebSignUpForm
from loyalty.presentation.web.flask_api.exc_handler import ERROR_CODE
from tests.e2e.api_client import TestAPIClient


async def test_ok(api_client: TestAPIClient, valid_business_signup_form: BusinessWebSignUpForm) -> None:
    resp = await api_client.sign_up_business(valid_business_signup_form)

    assert resp.http_response.status == 200
    assert resp.content is not None
    assert resp.content.business is not None

    assert resp.content.business.name == valid_business_signup_form.business_data.name
    assert resp.content.business.contact_phone == str(valid_business_signup_form.business_data.contact_phone)
    assert (
        resp.content.business.location
        == f"POINT(\
{float(valid_business_signup_form.business_data.lon)} {float(valid_business_signup_form.business_data.lat)})"
    )
    assert resp.content.business.contact_email == str(valid_business_signup_form.business_data.contact_email)


async def test_ok_without_phone(api_client: TestAPIClient, valid_business_signup_form: BusinessWebSignUpForm) -> None:
    valid_business_signup_form.business_data.contact_phone = None
    resp = await api_client.sign_up_business(valid_business_signup_form)

    assert resp.http_response.status == 200
    assert resp.content is not None
    assert resp.content.business is not None

    assert resp.content.business.contact_phone is None


async def test_already_exists_user(
    api_client: TestAPIClient,
    valid_business_signup_form: BusinessWebSignUpForm,
) -> None:
    resp = await api_client.sign_up_business(valid_business_signup_form)
    assert resp.http_response.status == 200

    valid_business_signup_form.business_data.name = "ajakdjdakj"
    resp_two = await api_client.sign_up_business(valid_business_signup_form)
    assert resp_two.http_response.status == 409

    assert resp_two.error is not None
    error_code = resp_two.error.get("unique_code")
    assert error_code is not None
    assert error_code == ERROR_CODE[UserAlreadyExistsError]


async def test_already_exists_name(
    api_client: TestAPIClient,
    valid_business_signup_form: BusinessWebSignUpForm,
) -> None:
    resp = await api_client.sign_up_business(valid_business_signup_form)
    assert resp.http_response.status == 200

    valid_business_signup_form.username = "ajakdkdha"
    resp_two = await api_client.sign_up_business(valid_business_signup_form)
    assert resp_two.http_response.status == 409

    assert resp_two.error is not None
    error_code = resp_two.error.get("unique_code")
    assert error_code is not None
    assert error_code == ERROR_CODE[BusinessAlreadyExistsError]
