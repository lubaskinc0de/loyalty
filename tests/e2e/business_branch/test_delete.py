from uuid import uuid4

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

    assert resp_create.content is not None

    business_branch = (
        await api_client.read_business_branch(
            src_business.business_id,
            resp_create.content.branch_id,
            token,
        )
    ).content

    assert business_branch is not None

    resp_delete = await api_client.delete_business_branch(
        src_business.business_id,
        business_branch.business_branch_id,
        token,
    )

    resp_read = await api_client.read_business_branch(
        src_business.business_id,
        business_branch.business_branch_id,
        token,
    )

    assert resp_delete.http_response.status == 204
    assert resp_read.http_response.status == 404


async def test_not_found(
    api_client: LoyaltyClient,
    business: BusinessUser,
) -> None:
    business_src, _, token = business
    resp = await api_client.delete_business_branch(business_src.business_id, uuid4(), token)
    assert resp.http_response.status == 404
