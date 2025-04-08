from dataclasses import dataclass
from typing import Literal, TypeVar

from adaptix import Retort
from aiohttp import ClientResponse, ClientSession

from loyalty.adapters.auth.provider import WebUserCredentials
from loyalty.application.business.create_business import BusinessForm
from loyalty.application.client.create_client import ClientForm
from loyalty.domain.entity.business import Business
from loyalty.domain.entity.client import Client
from loyalty.domain.entity.user import User
from loyalty.presentation.web.controller.login import TokenResponse

retort = Retort()
T = TypeVar("T")


def get_auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


@dataclass(slots=True, frozen=True)
class PingResponse:
    ping: Literal["pong"]


@dataclass(slots=True, frozen=True)
class APIResponse[T]:
    content: T | None
    http_response: ClientResponse
    error: dict[str, str] | None


@dataclass(slots=True, frozen=True)
class TestAPIClient:
    session: ClientSession

    async def _as_api_response[T](self, response: ClientResponse, model: type[T]) -> APIResponse[T]:
        return APIResponse(
            content=retort.load(await response.json(), model) if 200 >= response.status < 300 else None,
            http_response=response,
            error=await response.json() if response.status >= 400 else None,
        )

    async def ping(self) -> APIResponse[PingResponse]:
        url = "/ping/"
        async with self.session.get(url) as response:
            return await self._as_api_response(response, PingResponse)

    async def web_sign_up(self, data: WebUserCredentials) -> APIResponse[User]:
        url = "/user/web"
        async with self.session.post(url, json=data.model_dump(mode="json")) as response:
            return await self._as_api_response(response, User)

    async def create_client(self, data: ClientForm, token: str) -> APIResponse[Client]:
        url = "/client/"
        async with self.session.post(
            url,
            json=data.model_dump(mode="json"),
            headers=get_auth_headers(token),
        ) as response:
            return await self._as_api_response(response, Client)

    async def create_business(self, data: BusinessForm, token: str) -> APIResponse[Business]:
        url = "/business/"
        async with self.session.post(
            url,
            json=data.model_dump(mode="json"),
            headers=get_auth_headers(token),
        ) as response:
            return await self._as_api_response(response, Business)

    async def login(self, data: WebUserCredentials) -> APIResponse[TokenResponse]:
        url = "/user/login"
        async with self.session.post(url, json=data.model_dump(mode="json")) as response:
            return await self._as_api_response(response, TokenResponse)
