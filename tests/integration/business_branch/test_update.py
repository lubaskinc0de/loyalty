from uuid import uuid4

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.application.data_model.business_branch import BusinessBranchForm
from loyalty.application.shared_types import RussianPhoneNumber
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

    original_business_branch = (await api_client.read_business_branch(resp_create.content.branch_id)).content

    assert original_business_branch is not None

    business_branch_form.name = "CHANGED NAME OF OUR SUPER DUPER BUSINESS BRANCH"
    business_branch_form.contact_phone = RussianPhoneNumber("+79181778645")

    resp_update = await api_client.update_business_branch(
        original_business_branch.business_branch_id,
        business_branch_form,
    )

    assert resp_update.http_response.status == 204

    resp_read = await api_client.read_business_branch(original_business_branch.business_branch_id)

    updated_business_branch = resp_read.content

    assert updated_business_branch is not None
    assert updated_business_branch.name != original_business_branch.name
    assert updated_business_branch.contact_phone != original_business_branch.contact_phone

    assert updated_business_branch.name == business_branch_form.name
    assert str(updated_business_branch.contact_phone).replace("-", "").lstrip("tel:") == str(
        business_branch_form.contact_phone,
    )


async def test_not_found(
    api_client: LoyaltyClient,
    business: BusinessUser,
    business_branch_form: BusinessBranchForm,
) -> None:
    token = business[2]
    api_client.authorize(token)
    resp = await api_client.update_business_branch(uuid4(), business_branch_form)
    assert resp.http_response.status == 404


async def test_another_business(
    api_client: LoyaltyClient,
    business: BusinessUser,
    another_business: BusinessUser,
    business_branch_form: BusinessBranchForm,
) -> None:
    business_token = business[2]
    another_business_token = another_business[2]

    api_client.authorize(business_token)
    resp_create = await api_client.create_business_branch(business_branch_form)

    assert resp_create.content is not None

    original_business_branch = (await api_client.read_business_branch(resp_create.content.branch_id)).content

    assert original_business_branch is not None

    business_branch_form.name = "CHANGED NAME OF OUR SUPER DUPER BUSINESS BRANCH"
    business_branch_form.contact_phone = RussianPhoneNumber("+79181778645")

    api_client.authorize(another_business_token)
    resp_update = await api_client.update_business_branch(
        original_business_branch.business_branch_id,
        business_branch_form,
    )

    assert resp_update.http_response.status == 403


async def test_unauthorized(
    business: BusinessUser,
    api_client: LoyaltyClient,
    business_branch_form: BusinessBranchForm,
) -> None:
    token = business[2]

    api_client.authorize(token)
    branch_id = (await api_client.create_business_branch(business_branch_form)).unwrap().branch_id

    business_branch_form.name = "super mega new name"
    api_client.reset_authorization()
    (await api_client.update_business_branch(branch_id, business_branch_form)).except_status(401)
