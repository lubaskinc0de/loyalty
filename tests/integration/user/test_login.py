from loyalty.adapters.api_client import LoyaltyClient
from loyalty.adapters.auth.provider import WebUserCredentials
from loyalty.domain.entity.user import User


async def test_login_user(
    api_client: LoyaltyClient,
    user: User,
    auth_data: WebUserCredentials,
) -> None:
    token_response = await api_client.login(auth_data)
    assert token_response.http_response.status == 200
    assert token_response.content is not None
    assert token_response.content.user_id == user.user_id


async def test_login_bad_username(
    api_client: LoyaltyClient,
    user: User,  # noqa: ARG001
    auth_data: WebUserCredentials,
) -> None:
    auth_data.username = "bllbb"
    token_response = await api_client.login(auth_data)
    assert token_response.http_response.status == 403


async def test_login_bad_password(
    api_client: LoyaltyClient,
    user: User,  # noqa: ARG001
    auth_data: WebUserCredentials,
) -> None:
    auth_data.password = "aadjadljadlj"  # noqa: S105
    token_response = await api_client.login(auth_data)
    assert token_response.http_response.status == 403
