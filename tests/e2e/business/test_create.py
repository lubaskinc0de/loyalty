from loyalty.adapters.api_client import LoyaltyClient
from loyalty.application.business.create import BusinessForm
from tests.e2e.conftest import AuthorizedUser, BusinessUser


async def test_ok(api_client: LoyaltyClient, business_form: BusinessForm, authorized_user: AuthorizedUser) -> None:
    resp = await api_client.create_business(business_form, authorized_user[1])

    assert resp.http_response.status == 204


async def test_ok_without_phone(
    api_client: LoyaltyClient,
    business_form: BusinessForm,
    authorized_user: AuthorizedUser,
) -> None:
    business_form.contact_phone = None
    resp = await api_client.create_business(business_form, authorized_user[1])

    assert resp.http_response.status == 204


async def test_already_exists(
    api_client: LoyaltyClient,
    business: BusinessUser,
    business_form: BusinessForm,
) -> None:
    business_form.name = "akakadk"
    resp = await api_client.create_business(business_form, business[2])
    assert resp.http_response.status == 409


async def test_already_exists_name(
    api_client: LoyaltyClient,
    business: BusinessUser,
    business_form: BusinessForm,
) -> None:
    resp = await api_client.create_business(business_form, business[2])
    assert resp.http_response.status == 409
