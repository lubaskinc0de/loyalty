from dataclasses import dataclass
from typing import Literal, TypeVar

from adaptix import Retort
from aiohttp import ClientResponse, ClientSession

from loyalty.domain.entity.client import Client
from loyalty.presentation.web.controller.sign_up_client import ClientWebSignUpForm

retort = Retort()
T = TypeVar("T")


@dataclass(slots=True, frozen=True)
class PingResponse:
    ping: Literal["pong"]


@dataclass(slots=True, frozen=True)
class APIResponse[T]:
    content: T | None
    http_response: ClientResponse


@dataclass(slots=True, frozen=True)
class TestAPIClient:
    session: ClientSession

    async def _as_api_response[T](self, response: ClientResponse, model: type[T]) -> APIResponse[T]:
        return APIResponse(
            content=retort.load(await response.json(), model) if response.status == 200 else None,
            http_response=response,
        )

    async def ping(self) -> APIResponse[PingResponse]:
        url = "/ping/"
        async with self.session.get(url) as response:
            return await self._as_api_response(response, PingResponse)

    async def sign_up_client(self, data: ClientWebSignUpForm) -> APIResponse[Client]:
        url = "/client/"
        async with self.session.post(url, json=data.model_dump(mode="json")) as response:
            return await self._as_api_response(response, Client)
