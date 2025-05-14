from uuid import uuid4

import pytest

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.adapters.auth.provider import WebUserCredentials
from loyalty.application.client.create import ClientForm
from loyalty.application.data_model.business_branch import BusinessBranchForm
from tests.conftest import BusinessUser, create_authorized_user, create_client


async def test_ok_many(
    api_client: LoyaltyClient,
    business: BusinessUser,
    business_branch_form: BusinessBranchForm,
) -> None:
    src_business, _, token = business
    api_client.authorize(token)

    await api_client.create_business_branch(business_branch_form)

    business_branch_form.name = "Aaa"

    await api_client.create_business_branch(business_branch_form)

    resp = await api_client.read_business_branches(src_business.business_id)

    assert resp.http_response.status == 200
    assert resp.content is not None
    assert len(resp.content.branches) == 2


async def test_fake_business_many(
    api_client: LoyaltyClient,
    business: BusinessUser,
    business_branch_form: BusinessBranchForm,
) -> None:
    _, _, token = business
    api_client.authorize(token)

    await api_client.create_business_branch(business_branch_form)
    resp = await api_client.read_business_branches(uuid4())
    resp.except_status(404)


async def test_by_other_business_many(
    api_client: LoyaltyClient,
    business: BusinessUser,
    another_business: BusinessUser,
    business_branch_form: BusinessBranchForm,
) -> None:
    src_business, _, token = business
    api_client.authorize(token)

    await api_client.create_business_branch(business_branch_form)
    business_branch_form.name = "Aaa"
    await api_client.create_business_branch(business_branch_form)

    api_client.authorize(another_business[2])
    (await api_client.read_business_branches(src_business.business_id)).except_status(403)


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

    resp = await api_client.read_business_branch(business_branch.business_branch_id)

    assert resp.http_response.status == 200
    assert resp.content is not None
    assert resp.content == business_branch


async def test_forbidden(
    api_client: LoyaltyClient,
    business: BusinessUser,
    another_business: BusinessUser,
    business_branch_form: BusinessBranchForm,
) -> None:
    token = business[2]
    api_client.authorize(token)

    resp_create = (await api_client.create_business_branch(business_branch_form)).unwrap()
    api_client.authorize(another_business[2])

    (await api_client.read_business_branch(resp_create.branch_id)).except_status(403)


async def test_not_found(
    api_client: LoyaltyClient,
    business: BusinessUser,
) -> None:
    token = business[2]
    api_client.authorize(token)
    resp = await api_client.read_business_branch(uuid4())
    assert resp.http_response.status == 404


async def test_by_client(
    api_client: LoyaltyClient,
    business: BusinessUser,
    client_form: ClientForm,
    business_branch_form: BusinessBranchForm,
) -> None:
    business_token = business[2]

    client_user = await create_authorized_user(
        api_client,
        WebUserCredentials(
            username="someosskems",
            password="someeeeepasssswwww",  # noqa: S106
        ),
    )
    _, _, client_token = await create_client(api_client, client_form, client_user)

    api_client.authorize(business_token)

    resp_create = await api_client.create_business_branch(business_branch_form)

    assert resp_create.content is not None

    api_client.authorize(client_token)
    business_branch = (await api_client.read_business_branch(resp_create.content.branch_id)).content

    assert business_branch is not None

    resp = await api_client.read_business_branch(business_branch.business_branch_id)

    assert resp.http_response.status == 200
    assert resp.content is not None
    assert resp.content == business_branch


@pytest.mark.parametrize(
    ("limit", "offset"),
    [
        (-1, 0),
        (10, -1),
    ],
)
async def test_many_wrong_limit(
    api_client: LoyaltyClient,
    business: BusinessUser,
    business_branch_form: BusinessBranchForm,
    limit: int,
    offset: int,
) -> None:
    src_business, _, business_token = business

    api_client.authorize(business_token)
    (await api_client.create_business_branch(business_branch_form)).unwrap()

    business_branch_form.name = "Aaa"
    (await api_client.create_business_branch(business_branch_form)).unwrap()

    (
        await api_client.read_business_branches(
            business_id=src_business.business_id,
            limit=limit,
            offset=offset,
        )
    ).except_status(422)


async def test_unauthorized(
    business: BusinessUser,
    api_client: LoyaltyClient,
    business_branch_form: BusinessBranchForm,
) -> None:
    token = business[2]

    api_client.authorize(token)
    branch_id = (await api_client.create_business_branch(business_branch_form)).unwrap().branch_id

    api_client.reset_authorization()
    (await api_client.read_business_branch(branch_id)).except_status(401)


async def test_unauthorized_many(
    business: BusinessUser,
    api_client: LoyaltyClient,
    business_branch_form: BusinessBranchForm,
) -> None:
    src_busieness, _, token = business

    api_client.authorize(token)
    (await api_client.create_business_branch(business_branch_form)).unwrap()
    (await api_client.create_business_branch(business_branch_form)).unwrap()

    api_client.reset_authorization()
    (await api_client.read_business_branches(src_busieness.business_id)).except_status(401)
