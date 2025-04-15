from uuid import uuid4

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.adapters.auth.provider import WebUserCredentials
from loyalty.application.business_branch.create import BusinessBranchForm
from loyalty.application.client.create import ClientForm
from tests.e2e.conftest import BusinessUser, create_authorized_user, create_client


async def test_ok_many(
    api_client: LoyaltyClient,
    business: BusinessUser,
    business_branch_form: BusinessBranchForm,
) -> None:
    src_business, _, token = business
    await api_client.create_business_branch(src_business.business_id, business_branch_form, token)
    resp = await api_client.read_business_branches(src_business.business_id, token)
    assert resp.http_response.status == 200
    assert resp.content is not None
    assert len(resp.content.branches) != 0


async def test_ok(
    api_client: LoyaltyClient,
    business: BusinessUser,
    business_branch_form: BusinessBranchForm,
) -> None:
    src_business, _, token = business
    await api_client.create_business_branch(src_business.business_id, business_branch_form, token)
    business_branches = (await api_client.read_business_branches(src_business.business_id, token)).content

    assert business_branches is not None

    business_branch = business_branches.branches[0]

    resp = await api_client.read_business_branch(
        src_business.business_id,
        business_branch.business_branch_id,
        token,
    )

    assert resp.http_response.status == 200
    assert resp.content is not None
    assert resp.content == business_branch


async def test_not_found(
    api_client: LoyaltyClient,
    business: BusinessUser,
) -> None:
    business_src, _, token = business
    resp = await api_client.read_business_branch(business_src.business_id, uuid4(), token)
    assert resp.http_response.status == 404


async def test_by_client(
    api_client: LoyaltyClient,
    business: BusinessUser,
    client_form: ClientForm,
    business_branch_form: BusinessBranchForm,
) -> None:
    src_business, _, business_token = business

    client_user = await create_authorized_user(
        api_client,
        WebUserCredentials(
            username="someosskems",
            password="someeeeepasssswwww",  # noqa: S106
        ),
    )
    _, _, token = await create_client(api_client, client_form, client_user)

    await api_client.create_business_branch(src_business.business_id, business_branch_form, business_token)
    business_branches = (await api_client.read_business_branches(src_business.business_id, token)).content

    assert business_branches is not None

    business_branch = business_branches.branches[0]

    resp = await api_client.read_business_branch(
        src_business.business_id,
        business_branch.business_branch_id,
        token,
    )

    assert resp.http_response.status == 200
    assert resp.content is not None
    assert resp.content == business_branch
