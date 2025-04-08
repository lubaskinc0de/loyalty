from loyalty.application.business.create import BusinessForm
from tests.e2e.api_client import TestAPIClient
from tests.e2e.conftest import AuthorizedUser, BusinessUser


async def test_ok(api_client: TestAPIClient, business_form: BusinessForm, authorized_user: AuthorizedUser) -> None:
    resp = await api_client.create_business(business_form, authorized_user[1])

    assert resp.http_response.status == 200
    assert resp.content is not None

    assert resp.content.name == business_form.name
    assert resp.content.contact_phone == str(business_form.contact_phone)
    assert (
        resp.content.location
        == f"POINT(\
{float(business_form.lon)} {float(business_form.lat)})"
    )
    assert resp.content.contact_email == str(business_form.contact_email)


async def test_ok_without_phone(
    api_client: TestAPIClient,
    business_form: BusinessForm,
    authorized_user: AuthorizedUser,
) -> None:
    business_form.contact_phone = None
    resp = await api_client.create_business(business_form, authorized_user[1])

    assert resp.http_response.status == 200
    assert resp.content is not None
    assert resp.content.contact_phone is None


async def test_already_exists(
    api_client: TestAPIClient,
    business: BusinessUser,
    business_form: BusinessForm,
) -> None:
    business_form.name = "akakadk"
    resp = await api_client.create_business(business_form, business[2])
    assert resp.http_response.status == 409


async def test_already_exists_name(
    api_client: TestAPIClient,
    business: BusinessUser,
    business_form: BusinessForm,
) -> None:
    resp = await api_client.create_business(business_form, business[2])
    assert resp.http_response.status == 409
