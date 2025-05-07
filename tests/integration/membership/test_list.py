import pytest

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.adapters.auth.provider import WebUserCredentials
from loyalty.application.client.create import ClientForm
from loyalty.application.membership.create import MembershipForm
from loyalty.domain.entity.loyalty import Loyalty
from tests.conftest import ClientUser, create_authorized_user, create_client


@pytest.mark.parametrize(
    ("limit", "offset"),
    [
        (None, None),
        (1, 0),
        (2, None),
        (3, 0),
        (1, 1),
        (1, 2),
    ],
)
async def test_ok(
    api_client: LoyaltyClient,
    client: ClientUser,
    loyalties: list[Loyalty],
    limit: int | None,
    offset: int | None,
) -> None:
    api_client.authorize(client[2])
    for loyalty in loyalties:
        (
            await api_client.create_membership(
                MembershipForm(
                    loyalty_id=loyalty.loyalty_id,
                ),
            )
        ).unwrap()

    result = (await api_client.read_memberships(limit, offset)).unwrap()
    expected_ids = [x.loyalty_id for x in loyalties]

    if offset:
        expected_ids = expected_ids[offset:]

    if limit:
        expected_ids = expected_ids[:limit]

    result_ids = [x.loyalty.loyalty_id for x in result]
    assert expected_ids == result_ids

    for each in result:
        assert each.client.client_id == client[0].client_id


async def test_by_other_client(
    api_client: LoyaltyClient,
    loyalties: list[Loyalty],
    auth_data: WebUserCredentials,
    client: ClientUser,
    client_form: ClientForm,
) -> None:
    auth_data.username = "akakakaka"
    new_client = await create_client(api_client, client_form, await create_authorized_user(api_client, auth_data))

    api_client.authorize(client[2])
    for loyalty in loyalties:
        (
            await api_client.create_membership(
                MembershipForm(
                    loyalty_id=loyalty.loyalty_id,
                ),
            )
        ).unwrap()

    api_client.authorize(new_client[2])
    result = (await api_client.read_memberships()).unwrap()
    assert result == []


async def test_empty(
    api_client: LoyaltyClient,
    client: ClientUser,
) -> None:
    api_client.authorize(client[2])
    assert (await api_client.read_memberships()).unwrap() == []


async def test_unauthorized(
    api_client: LoyaltyClient,
) -> None:
    api_client.reset_authorization()
    (await api_client.read_memberships()).except_status(401)
