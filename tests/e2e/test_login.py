from loyalty.presentation.web.controller.sign_up_business import BusinessWebSignUpForm
from loyalty.presentation.web.controller.sign_up_client import ClientWebSignUpForm
from loyalty.presentation.web.controller.user import WebUserCredentials
from tests.e2e.api_client import TestAPIClient
from tests.e2e.conftest import create_business, create_client


async def test_login_user(
    api_client: TestAPIClient,
    valid_client_signup_form: ClientWebSignUpForm,
) -> None:
    creds = WebUserCredentials(
        username=valid_client_signup_form.username,
        password=valid_client_signup_form.password,
    )
    client = await create_client(api_client, valid_client_signup_form)

    token_response = await api_client.login(creds)
    assert token_response.http_response.status == 200
    assert token_response.content is not None
    assert token_response.content.token_info.entity_id == client.client_id
    assert token_response.content.token_info.role == "client"


async def test_login_business(
    api_client: TestAPIClient,
    valid_business_signup_form: BusinessWebSignUpForm,
) -> None:
    creds = WebUserCredentials(
        username=valid_business_signup_form.username,
        password=valid_business_signup_form.password,
    )
    business = await create_business(api_client, valid_business_signup_form)

    token_response = await api_client.login(creds)
    assert token_response.http_response.status == 200
    assert token_response.content is not None
    assert token_response.content.token_info.entity_id == business.business_id
    assert token_response.content.token_info.role == "business"


async def test_login_incorrect_username(
    api_client: TestAPIClient,
    valid_business_signup_form: BusinessWebSignUpForm,
) -> None:
    creds = WebUserCredentials(
        username="blalblalbl",
        password=valid_business_signup_form.password,
    )
    await create_business(api_client, valid_business_signup_form)

    token_response = await api_client.login(creds)
    assert token_response.http_response.status == 403


async def test_login_incorrect_password(
    api_client: TestAPIClient,
    valid_business_signup_form: BusinessWebSignUpForm,
) -> None:
    creds = WebUserCredentials(
        username=valid_business_signup_form.username,
        password="blLLLS",  # noqa: S106
    )
    await create_business(api_client, valid_business_signup_form)

    token_response = await api_client.login(creds)
    assert token_response.http_response.status == 403
