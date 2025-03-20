import json
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

    async def ping(self) -> APIResponse[str]:
        url = "/ping/"
        async with self.session.get(url) as response:
            return APIResponse(content=json.loads(await response.text()), http_response=response)
