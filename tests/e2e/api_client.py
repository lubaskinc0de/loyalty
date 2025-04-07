from dataclasses import dataclass
from typing import Literal, TypeVar

from adaptix import Retort
from aiohttp import ClientResponse, ClientSession

from loyalty.adapters.auth.access_token import AccessToken
from loyalty.presentation.web.controller.sign_up_business import BusinessWebSignUpForm, CreatedBusiness
from loyalty.presentation.web.controller.sign_up_client import ClientWebSignUpForm, CreatedClient
from loyalty.presentation.web.controller.user import WebUserCredentials

retort = Retort()
T = TypeVar("T")


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

    async def sign_up_client(self, data: ClientWebSignUpForm) -> APIResponse[CreatedClient]:
        url = "/client/"
        async with self.session.post(url, json=data.model_dump(mode="json")) as response:
            return await self._as_api_response(response, CreatedClient)

    async def sign_up_business(self, data: BusinessWebSignUpForm) -> APIResponse[CreatedBusiness]:
        url = "/business/"
        async with self.session.post(url, json=data.model_dump(mode="json")) as response:
            return await self._as_api_response(response, CreatedBusiness)

    async def login(self, data: WebUserCredentials) -> APIResponse[AccessToken]:
        url = "/user/"
        async with self.session.post(url, json=data.model_dump(mode="json")) as response:
            return await self._as_api_response(response, AccessToken)
