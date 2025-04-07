import pytest
from pydantic_extra_types.coordinate import Latitude, Longitude

from loyalty.application.business.create_business import BusinessForm
from loyalty.application.shared_types import RussianPhoneNumber
from loyalty.domain.entity.business import Business
from loyalty.presentation.web.controller.sign_up_business import BusinessWebSignUpForm
from tests.e2e.api_client import TestAPIClient


@pytest.fixture
def valid_signup_form() -> BusinessWebSignUpForm:
    return BusinessWebSignUpForm(
        username="lubaskin business",
        password="coolpassw",  # noqa: S106
        business_data=BusinessForm(
            name="Ilya Lyubavskiy Business",
            lat=Latitude(55.7522),
            lon=Longitude(37.6156),
            contact_phone=RussianPhoneNumber("+79281778645"),
            contact_email="structnull@yandex.ru",
        ),
    )


@pytest.fixture
async def business(api_client: TestAPIClient, valid_signup_form: BusinessWebSignUpForm) -> Business:
    resp = await api_client.sign_up_business(valid_signup_form)
    assert resp.http_response.status == 200
    assert resp.content is not None

    return resp.content
