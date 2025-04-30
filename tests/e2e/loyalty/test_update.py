from uuid import uuid4

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.application.data_model.loyalty import LoyaltyForm
from loyalty.domain.shared_types import Gender
from tests.e2e.conftest import BusinessUser


async def test_ok(
    api_client: LoyaltyClient,
    business: BusinessUser,
    loyalty_form: LoyaltyForm,
) -> None:
    token = business[2]
    resp_create = await api_client.create_loyalty(loyalty_form, token)

    assert resp_create.content is not None

    original_loyalty = (
        await api_client.read_loyalty(
            resp_create.content.loyalty_id,
            token,
        )
    ).content

    assert original_loyalty is not None
    
    loyalty_form.description = "не, маунтин дью круче"
    loyalty_form.gender = Gender.FEMALE
    
    resp_update = await api_client.update_loyalty(
        original_loyalty.loyalty_id,
        loyalty_form,
        token,
    )

    assert resp_update.http_response.status == 204

    resp_read = await api_client.read_loyalty(
        original_loyalty.loyalty_id,
        token,
    )

    updated_loyalty = resp_read.content

    assert updated_loyalty is not None
    
    assert updated_loyalty.description == loyalty_form.description
    assert updated_loyalty.gender == loyalty_form.gender

    assert updated_loyalty.name == original_loyalty.name
    assert updated_loyalty.starts_at == original_loyalty.starts_at
    assert updated_loyalty.ends_at == original_loyalty.ends_at
    assert updated_loyalty.money_per_bonus == original_loyalty.money_per_bonus
    assert updated_loyalty.min_age == original_loyalty.min_age
    assert updated_loyalty.max_age == original_loyalty.max_age
    assert updated_loyalty.is_active == original_loyalty.is_active
    

async def test_not_found(
    api_client: LoyaltyClient,
    business: BusinessUser,
    loyalty_form: LoyaltyForm,
) -> None:
    token = business[2]
    resp = await api_client.update_loyalty(uuid4(), loyalty_form, token)
    assert resp.http_response.status == 404



async def test_another_business(
    api_client: LoyaltyClient,
    business: BusinessUser,
    another_business: BusinessUser,
    loyalty_form: LoyaltyForm,
) -> None:
    token = business[2]
    another_business_token = another_business[2]
    resp_create = await api_client.create_loyalty(loyalty_form, token)

    assert resp_create.content is not None

    original_loyalty = (
        await api_client.read_loyalty(
            resp_create.content.loyalty_id,
            token,
        )
    ).content

    assert original_loyalty is not None

    loyalty_form.description = "не, маунтин дью круче"
    loyalty_form.gender = Gender.FEMALE

    resp_update = await api_client.update_loyalty(
        original_loyalty.loyalty_id,
        loyalty_form,
        another_business_token,
    )

    assert resp_update.http_response.status == 403
