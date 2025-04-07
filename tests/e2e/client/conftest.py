import pytest
from pydantic_extra_types.coordinate import Latitude, Longitude

from loyalty.application.create_client import ClientForm
from loyalty.application.shared_types import RussianPhoneNumber
from loyalty.domain.shared_types import Gender
from loyalty.presentation.web.controller.sign_up import ClientWebSignUpForm


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
