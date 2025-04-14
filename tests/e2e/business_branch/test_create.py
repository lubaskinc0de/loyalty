from loyalty.adapters.api_client import LoyaltyClient
from loyalty.application.business_branch.create import BusinessBranchForm
from tests.e2e.conftest import AuthorizedUser, BusinessUser


async def test_ok(
    api_client: LoyaltyClient,
    business: BusinessUser,
    business_branch_form: BusinessBranchForm,
    authorized_user: AuthorizedUser,
) -> None:
    resp = await api_client.create_business_branch(business[0].business_id, business_branch_form, authorized_user[1])

    assert resp.http_response.status == 204


async def test_ok_without_phone(
    api_client: LoyaltyClient,
    business: BusinessUser,
    business_branch_form: BusinessBranchForm,
    authorized_user: AuthorizedUser,
) -> None:
    business_branch_form.contact_phone = None
    resp = await api_client.create_business_branch(business[0].business_id, business_branch_form, authorized_user[1])

    assert resp.http_response.status == 204
