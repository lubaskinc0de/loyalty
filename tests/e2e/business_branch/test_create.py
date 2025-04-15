from loyalty.adapters.api_client import LoyaltyClient
from loyalty.application.business_branch.create import BusinessBranchForm
from tests.e2e.conftest import BusinessUser


async def test_ok(
    api_client: LoyaltyClient,
    business: BusinessUser,
    business_branch_form: BusinessBranchForm,
) -> None:
    src_business, _, token = business
    resp_create = await api_client.create_business_branch(src_business.business_id, business_branch_form, token)

    assert resp_create.http_response.status == 200
    assert resp_create.content is not None

    resp_read = await api_client.read_business_branch(src_business.business_id, resp_create.content.branch_id, token)

    created_business_branch = resp_read.content

    assert created_business_branch is not None

    assert business_branch_form.name == created_business_branch.name
    assert business_branch_form.address == created_business_branch.address
    assert business_branch_form.contact_phone == created_business_branch.contact_phone


async def test_ok_without_phone(
    api_client: LoyaltyClient,
    business: BusinessUser,
    business_branch_form: BusinessBranchForm,
) -> None:
    src_business, _, token = business
    business_branch_form.contact_phone = None

    resp_create = await api_client.create_business_branch(src_business.business_id, business_branch_form, token)

    assert resp_create.http_response.status == 200
    assert resp_create.content is not None

    resp_read = await api_client.read_business_branch(src_business.business_id, resp_create.content.branch_id, token)

    created_business_branch = resp_read.content

    assert created_business_branch is not None

    assert business_branch_form.name == created_business_branch.name
    assert business_branch_form.address == created_business_branch.address
    assert created_business_branch.contact_phone is None
