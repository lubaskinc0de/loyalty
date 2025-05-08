from uuid import uuid4

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.application.data_model.business_branch import BusinessBranchForm
from tests.conftest import BusinessUser


async def test_ok(
    api_client: LoyaltyClient,
    business: BusinessUser,
    business_branch_form: BusinessBranchForm,
) -> None:
    token = business[2]
    api_client.authorize(token)

    resp_create = await api_client.create_business_branch(business_branch_form)

    assert resp_create.content is not None

    business_branch = (await api_client.read_business_branch(resp_create.content.branch_id)).content

    assert business_branch is not None

    resp_delete = await api_client.delete_business_branch(business_branch.business_branch_id)

    resp_read = await api_client.read_business_branch(business_branch.business_branch_id)

    assert resp_delete.http_response.status == 204
    assert resp_read.http_response.status == 404


async def test_not_found(
    api_client: LoyaltyClient,
    business: BusinessUser,
) -> None:
    token = business[2]
    api_client.authorize(token)
    resp = await api_client.delete_business_branch(uuid4())
    assert resp.http_response.status == 404


async def test_another_business(
    api_client: LoyaltyClient,
    business: BusinessUser,
    another_business: BusinessUser,
    business_branch_form: BusinessBranchForm,
) -> None:
    token = business[2]
    another_business_token = another_business[2]

    api_client.authorize(token)
    resp_create = await api_client.create_business_branch(business_branch_form)

    assert resp_create.content is not None

    business_branch = (await api_client.read_business_branch(resp_create.content.branch_id)).content

    assert business_branch is not None

    api_client.authorize(another_business_token)
    resp_delete = await api_client.delete_business_branch(business_branch.business_branch_id)

    assert resp_delete.http_response.status == 403


async def test_unauthorized(
    business: BusinessUser, api_client: LoyaltyClient, business_branch_form: BusinessBranchForm,
) -> None:
    token = business[2]

    api_client.authorize(token)
    branch_id = (await api_client.create_business_branch(business_branch_form)).unwrap().branch_id

    api_client.reset_authorization()
    (await api_client.delete_business_branch(branch_id)).except_status(401)
