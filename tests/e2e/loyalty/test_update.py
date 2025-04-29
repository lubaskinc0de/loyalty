from uuid import uuid4

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.application.data_model.loyalty import LoyaltyForm
from tests.e2e.conftest import BusinessUser

# async def test_ok(
#     api_client: LoyaltyClient,
#     business: BusinessUser,
#     loyalty_form: LoyaltyForm,
# ) -> None:
#     token = business[2]
#     resp_create = await api_client.create_loyalty(loyalty_form, token)

#     assert resp_create.content is not None

#     original_loyalty = (
#         await api_client.read_loyalty(
#             resp_create.content.loyalty_id,
#             token,
#         )
#     ).content

#     assert original_loyalty is not None

#     original_loyalty.description = "не, маунтин дью круче"
#     original_loyalty.gender = Gender.FEMALE

#     resp_update = await api_client.update_loyalty(
#         original_loyalty.loyalty_id,
#         loyalty_form,
#         token,
#     )

#     assert resp_update.http_response.status == 204

#     resp_read = await api_client.read_loyalty(
#         original_loyalty.loyalty_id,
#         token,
#     )

#     updated_loyalty = resp_read.content

#     assert updated_loyalty is not None
#     assert updated_loyalty.description != loyalty_form.description
#     assert updated_loyalty.gender != loyalty_form.contact_phone

#     assert updated_loyalty.name == loyalty_form.name
#     assert updated_loyalty.starts_at == loyalty_form.starts_at
#     assert updated_loyalty.ends_at == loyalty_form.ends_at
#     assert updated_loyalty.money_per_bonus == loyalty_form.money_per_bonus
#     assert updated_loyalty.min_age == loyalty_form.min_age
#     assert updated_loyalty.max_age == loyalty_form.max_age
#     assert updated_loyalty.is_active == loyalty_form.is_active


async def test_not_found(
    api_client: LoyaltyClient,
    business: BusinessUser,
    loyalty_form: LoyaltyForm,
) -> None:
    token = business[2]
    resp = await api_client.update_loyalty(uuid4(), loyalty_form, token)
    assert resp.http_response.status == 404
