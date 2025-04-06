from dataclasses import dataclass
from typing import Generic, TypeVar

from adaptix import Retort
from aiohttp import ClientResponse, ClientSession

retort = Retort()
T = TypeVar("T")


@dataclass(slots=True, frozen=True)
class APIResponse(Generic[T]):
    content: T
    http_response: ClientResponse


@dataclass(slots=True, frozen=True)
class TestAPIClient:
    session: ClientSession

    async def ping(self) -> APIResponse[dict[str, str]]:
        url = "/ping/"
        async with self.session.get(url) as response:
            return APIResponse(content=await response.json(), http_response=response)
