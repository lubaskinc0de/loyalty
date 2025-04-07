import pytest
from pydantic_extra_types.coordinate import Latitude, Longitude

from loyalty.application.client.create_client import ClientForm
from loyalty.application.shared_types import RussianPhoneNumber
from loyalty.domain.entity.client import Client
from loyalty.domain.shared_types import Gender
from loyalty.presentation.web.controller.sign_up_client import ClientWebSignUpForm
from tests.e2e.api_client import TestAPIClient


@pytest.fixture
def valid_signup_form() -> ClientWebSignUpForm:
    return ClientWebSignUpForm(
        username="lubaskin",
        password="coolpassw",  # noqa: S106
        client_data=ClientForm(
            full_name="Ilya Lyubavskiy",
            age=20,
            lat=Latitude(55.7522),
            lon=Longitude(37.6156),
            gender=Gender.MALE,
            phone=RussianPhoneNumber("+79281778645"),
        ),
    )


@pytest.fixture
async def client(api_client: TestAPIClient, valid_signup_form: ClientWebSignUpForm) -> Client:
    resp = await api_client.sign_up_client(valid_signup_form)
    assert resp.http_response.status == 200
    assert resp.content is not None

    return resp.content
