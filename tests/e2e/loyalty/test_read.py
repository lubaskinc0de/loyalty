from uuid import uuid4

from loyalty.adapters.api_client import LoyaltyClient
from loyalty.adapters.auth.provider import WebUserCredentials
from loyalty.application.client.create import ClientForm
from loyalty.application.data_model.loyalty import LoyaltyForm
from loyalty.domain.shared_types import Gender, LoyaltyTimeFrame
from tests.e2e.conftest import BusinessUser, create_authorized_user, create_client


async def test_ok_by_client_many_with_business(
    api_client: LoyaltyClient,
    business: BusinessUser,
    client_form: ClientForm,
    loyalty_form: LoyaltyForm,
    another_business: BusinessUser,
) -> None:
    src_business, _, business_token = business
    another_business_token = another_business[2]

    client_user = await create_authorized_user(
        api_client,
        WebUserCredentials(
            username="someosskems",
            password="someeeeepasssswwww",  # noqa: S106
        ),
    )
    _, _, client_token = await create_client(api_client, client_form, client_user)

    api_client.authorize(business_token)

    await api_client.create_loyalty(loyalty_form)

    loyalty_form.name = "Aaa"

    await api_client.create_loyalty(loyalty_form)

    api_client.authorize(another_business_token)
    loyalty_form.name = "Bbb"

    await api_client.create_loyalty(loyalty_form)

    api_client.authorize(client_token)
    resp = await api_client.read_loyalties(
        time_frame=LoyaltyTimeFrame.ALL,
        business_id=src_business.business_id,
    )

    assert resp.http_response.status == 200
    assert resp.content is not None
    assert len(resp.content.loyalties) == 2


async def test_many_by_client_many(
    api_client: LoyaltyClient,
    business: BusinessUser,
    client_form: ClientForm,
    loyalty_form: LoyaltyForm,
    another_business: BusinessUser,
) -> None:
    _, _, business_token = business
    another_business_token = another_business[2]

    client_user = await create_authorized_user(
        api_client,
        WebUserCredentials(
            username="someosskems",
            password="someeeeepasssswwww",  # noqa: S106
        ),
    )
    _, _, client_token = await create_client(api_client, client_form, client_user)

    api_client.authorize(business_token)
    await api_client.create_loyalty(loyalty_form)

    loyalty_form.name = "Aaa"

    await api_client.create_loyalty(loyalty_form)

    api_client.authorize(another_business_token)
    loyalty_form.name = "Bbb"

    await api_client.create_loyalty(loyalty_form)

    api_client.authorize(client_token)
    resp = await api_client.read_loyalties(time_frame=LoyaltyTimeFrame.ALL)

    assert resp.http_response.status == 200
    assert resp.content is not None
    assert len(resp.content.loyalties) == 3


async def test_many_by_client_many_with_gender(
    api_client: LoyaltyClient,
    business: BusinessUser,
    client_form: ClientForm,
    loyalty_form: LoyaltyForm,
) -> None:
    _, _, business_token = business

    client_user = await create_authorized_user(
        api_client,
        WebUserCredentials(
            username="someosskems",
            password="someeeeepasssswwww",  # noqa: S106
        ),
    )
    _, _, client_token = await create_client(api_client, client_form, client_user)

    api_client.authorize(business_token)
    await api_client.create_loyalty(loyalty_form)

    loyalty_form.name = "Aaa"
    loyalty_form.gender = Gender.MALE

    await api_client.create_loyalty(loyalty_form)

    loyalty_form.name = "Bbb"
    loyalty_form.gender = Gender.FEMALE

    await api_client.create_loyalty(loyalty_form)

    api_client.authorize(client_token)
    resp = await api_client.read_loyalties(time_frame=LoyaltyTimeFrame.ALL)

    assert resp.http_response.status == 200
    assert resp.content is not None
    assert len(resp.content.loyalties) == 2


async def test_many_by_client_many_with_active(
    api_client: LoyaltyClient,
    business: BusinessUser,
    client_form: ClientForm,
    loyalty_form: LoyaltyForm,
    another_business: BusinessUser,
) -> None:
    _, _, business_token = business
    another_business_token = another_business[2]

    client_user = await create_authorized_user(
        api_client,
        WebUserCredentials(
            username="someosskems",
            password="someeeeepasssswwww",  # noqa: S106
        ),
    )
    _, _, client_token = await create_client(api_client, client_form, client_user)

    api_client.authorize(business_token)
    await api_client.create_loyalty(loyalty_form)

    loyalty_form.name = "Aaa"

    await api_client.create_loyalty(loyalty_form)

    api_client.authorize(another_business_token)
    loyalty_form.name = "Bbb"
    loyalty_form.is_active = True

    await api_client.create_loyalty(loyalty_form)

    api_client.authorize(client_token)
    resp = await api_client.read_loyalties(active=False, time_frame=LoyaltyTimeFrame.ALL)

    assert resp.http_response.status == 200
    assert resp.content is not None
    assert len(resp.content.loyalties) == 2


async def test_ok(
    api_client: LoyaltyClient,
    business: BusinessUser,
    loyalty_form: LoyaltyForm,
) -> None:
    token = business[2]
    api_client.authorize(token)

    resp_create = await api_client.create_loyalty(loyalty_form)

    assert resp_create.content is not None

    resp = await api_client.read_loyalty(resp_create.content.loyalty_id)

    assert resp.http_response.status == 200
    assert resp.content is not None


async def test_not_found(
    api_client: LoyaltyClient,
    business: BusinessUser,
) -> None:
    token = business[2]
    api_client.authorize(token)
    resp = await api_client.read_loyalty(uuid4())
    assert resp.http_response.status == 404


async def test_by_client(
    api_client: LoyaltyClient,
    business: BusinessUser,
    client_form: ClientForm,
    loyalty_form: LoyaltyForm,
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
    resp_create = await api_client.create_loyalty(loyalty_form)

    assert resp_create.content is not None

    api_client.authorize(client_token)
    loyalty = (await api_client.read_loyalty(resp_create.content.loyalty_id)).content

    assert loyalty is not None

    resp = await api_client.read_loyalty(loyalty.loyalty_id)

    assert resp.http_response.status == 200
    assert resp.content is not None
    assert resp.content == loyalty
