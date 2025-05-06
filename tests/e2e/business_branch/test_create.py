from loyalty.adapters.api_client import LoyaltyClient
from loyalty.application.data_model.business_branch import BusinessBranchForm
from tests.e2e.conftest import BusinessUser


async def test_ok(
    api_client: LoyaltyClient,
    business: BusinessUser,
    business_branch_form: BusinessBranchForm,
) -> None:
    token = business[2]
    api_client.authorize(token)
    resp_create = await api_client.create_business_branch(business_branch_form)

    assert resp_create.http_response.status == 200
    assert resp_create.content is not None

    resp_read = await api_client.read_business_branch(resp_create.content.branch_id)

    created_business_branch = resp_read.content

    assert created_business_branch is not None

    assert business_branch_form.name == created_business_branch.name
    assert business_branch_form.contact_phone == created_business_branch.contact_phone


async def test_ok_without_phone(
    api_client: LoyaltyClient,
    business: BusinessUser,
    business_branch_form: BusinessBranchForm,
) -> None:
    token = business[2]
    business_branch_form.contact_phone = None
    api_client.authorize(token)

    resp_create = await api_client.create_business_branch(business_branch_form)

    assert resp_create.http_response.status == 200
    assert resp_create.content is not None

    resp_read = await api_client.read_business_branch(resp_create.content.branch_id)

    created_business_branch = resp_read.content

    assert created_business_branch is not None

    assert business_branch_form.name == created_business_branch.name
    assert created_business_branch.contact_phone is None
