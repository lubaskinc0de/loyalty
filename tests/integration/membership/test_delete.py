from uuid import uuid4

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.adapters.auth.provider import WebUserCredentials
from loyalty.application.business.create import BusinessForm
from loyalty.application.client.create import ClientForm
from loyalty.application.shared_types import RussianPhoneNumber
from loyalty.domain.entity.membership import LoyaltyMembership
from tests.conftest import ClientUser, create_authorized_user, create_business, create_client


async def test_ok(api_client: LoyaltyClient, membership: LoyaltyMembership, client: ClientUser) -> None:
    api_client.authorize(client[2])
    (await api_client.delete_membership(membership.membership_id)).except_status(204)
    (await api_client.read_membership(membership.membership_id)).except_status(404)


async def test_not_exist(api_client: LoyaltyClient, client: ClientUser) -> None:
    api_client.authorize(client[2])
    (await api_client.delete_membership(uuid4())).except_status(404)


async def test_by_business(
    api_client: LoyaltyClient,
    membership: LoyaltyMembership,
    auth_data: WebUserCredentials,
    business_form: BusinessForm,
) -> None:
    auth_data.username = "ajadjdajdladjldl"
    business_form.name = "ajaldjladjda"
    business = await create_business(
        api_client,
        business_form=business_form,
        authorized_user=await create_authorized_user(api_client, auth_data),
    )
    api_client.authorize(business[2])
    (await api_client.delete_membership(membership.membership_id)).except_status(403)


async def test_by_other_client(
    api_client: LoyaltyClient,
    membership: LoyaltyMembership,
    client_form: ClientForm,
    auth_data: WebUserCredentials,
) -> None:
    client_form.phone = RussianPhoneNumber("+78005553535")
    auth_data.username = "ajadjdajdladjldl"
    client2 = await create_client(api_client, client_form, await create_authorized_user(api_client, auth_data))

    api_client.authorize(client2[2])
    (await api_client.delete_membership(membership.membership_id)).except_status(403)


async def test_unauthorized(api_client: LoyaltyClient, membership: LoyaltyMembership) -> None:
    api_client.reset_authorization()
    (await api_client.delete_membership(membership.membership_id)).except_status(401)
