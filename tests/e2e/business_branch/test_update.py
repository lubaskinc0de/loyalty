from loyalty.adapters.api_client import LoyaltyClient
from loyalty.application.business_branch.create import BusinessBranchForm
from tests.e2e.conftest import BusinessUser


async def test_ok(
    api_client: LoyaltyClient,
    business: BusinessUser,
    business_branch_form: BusinessBranchForm,
) -> None:
    src_business, _, token = business
    await api_client.create_business_branch(src_business.business_id, business_branch_form, token)
    business_branches = (await api_client.read_business_branches(src_business.business_id, token)).content

    assert business_branches is not None

    original_business_branch = business_branches.branches[0]

    business_branch_form.name = "CHANGED NAME OF OUR SUPER DUPER BUSINESS BRANCH"

    resp_update = await api_client.update_business_branch(
        src_business.business_id, original_business_branch.business_branch_id, business_branch_form, token,
    )

    assert resp_update.http_response.status == 204

    resp_read = await api_client.read_business_branch(
        src_business.business_id,
        original_business_branch.business_branch_id,
        token,
    )

    assert resp_read.content != original_business_branch
