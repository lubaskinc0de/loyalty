from uuid import uuid4

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.application.business_branch.create import BusinessBranchForm
from loyalty.application.shared_types import RussianPhoneNumber
from tests.e2e.conftest import BusinessUser


async def test_ok(
    api_client: LoyaltyClient,
    business: BusinessUser,
    business_branch_form: BusinessBranchForm,
) -> None:
    token = business[2]
    resp_create = await api_client.create_business_branch(business_branch_form, token)

    assert resp_create.content is not None

    original_business_branch = (
        await api_client.read_business_branch(
            resp_create.content.branch_id,
            token,
        )
    ).content

    assert original_business_branch is not None

    business_branch_form.name = "CHANGED NAME OF OUR SUPER DUPER BUSINESS BRANCH"
    business_branch_form.contact_phone = RussianPhoneNumber("+79181778645")

    resp_update = await api_client.update_business_branch(
        original_business_branch.business_branch_id,
        business_branch_form,
        token,
    )

    assert resp_update.http_response.status == 204

    resp_read = await api_client.read_business_branch(
        original_business_branch.business_branch_id,
        token,
    )

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
    resp = await api_client.update_business_branch(uuid4(), business_branch_form, token)
    assert resp.http_response.status == 404


async def test_another_business(
    api_client: LoyaltyClient,
    business: BusinessUser,
    another_business: BusinessUser,
    business_branch_form: BusinessBranchForm,
) -> None:
    token = business[2]
    another_business_token = another_business[2]
    resp_create = await api_client.create_business_branch(business_branch_form, token)

    assert resp_create.content is not None

    original_business_branch = (
        await api_client.read_business_branch(
            resp_create.content.branch_id,
            token,
        )
    ).content

    assert original_business_branch is not None

    business_branch_form.name = "CHANGED NAME OF OUR SUPER DUPER BUSINESS BRANCH"
    business_branch_form.contact_phone = RussianPhoneNumber("+79181778645")

    resp_update = await api_client.update_business_branch(
        original_business_branch.business_branch_id,
        business_branch_form,
        another_business_token,
    )

    assert resp_update.http_response.status == 403
