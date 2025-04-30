from dataclasses import dataclass
from typing import Literal, TypeVar
from uuid import UUID

from adaptix import Retort
from aiohttp import ClientResponse, ClientSession

from loyalty.adapters.api_models import BusinessBranchId, BusinessBranchList, LoyaltyId
from loyalty.adapters.auth.provider import WebUserCredentials
from loyalty.application.business.create import BusinessForm
from loyalty.application.business_branch.create import BusinessBranchForm
from loyalty.application.client.create import ClientForm
from loyalty.application.data_model.loyalty import LoyaltyForm
from loyalty.domain.entity.business import Business
from loyalty.domain.entity.business_branch import BusinessBranch
from loyalty.domain.entity.client import Client
from loyalty.domain.entity.loyalty import Loyalty
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
class LoyaltyClient:
    session: ClientSession

    async def _as_api_response[T](self, response: ClientResponse, model: type[T] | None = None) -> APIResponse[T]:
        return APIResponse(
            content=retort.load(await response.json(), model)
            if 200 >= response.status < 300 and model is not None
            else None,
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

    async def create_client(self, data: ClientForm, token: str) -> APIResponse[None]:
        url = "/client/"
        async with self.session.post(
            url,
            json=data.model_dump(mode="json"),
            headers=get_auth_headers(token),
        ) as response:
            return await self._as_api_response(response)

    async def create_business(self, data: BusinessForm, token: str) -> APIResponse[None]:
        url = "/business/"
        async with self.session.post(
            url,
            json=data.model_dump(mode="json"),
            headers=get_auth_headers(token),
        ) as response:
            return await self._as_api_response(response)

    async def create_business_branch(
        self,
        data: BusinessBranchForm,
        token: str,
    ) -> APIResponse[BusinessBranchId]:
        url = "/branch"
        async with self.session.post(
            url,
            json=data.model_dump(mode="json"),
            headers=get_auth_headers(token),
        ) as response:
            return await self._as_api_response(response, BusinessBranchId)

    async def create_loyalty(
        self,
        data: LoyaltyForm,
        token: str,
    ) -> APIResponse[LoyaltyId]:
        url = "/loyalty"
        async with self.session.post(
            url,
            json=data.model_dump(mode="json"),
            headers=get_auth_headers(token),
        ) as response:
            return await self._as_api_response(response, LoyaltyId)

    async def login(self, data: WebUserCredentials) -> APIResponse[TokenResponse]:
        url = "/user/login"
        async with self.session.post(url, json=data.model_dump(mode="json")) as response:
            return await self._as_api_response(response, TokenResponse)

    async def read_client(self, token: str) -> APIResponse[Client]:
        url = "/client/"
        async with self.session.get(
            url,
            headers=get_auth_headers(token),
        ) as response:
            return await self._as_api_response(response, Client)

    async def read_user(self, token: str) -> APIResponse[User]:
        url = "/user/"
        async with self.session.get(
            url,
            headers=get_auth_headers(token),
        ) as response:
            return await self._as_api_response(response, User)

    async def read_business(self, business_id: UUID, token: str) -> APIResponse[Business]:
        url = f"/business/{business_id}"
        async with self.session.get(
            url,
            headers=get_auth_headers(token),
        ) as response:
            return await self._as_api_response(response, Business)

    async def read_loyalty(self, loyalty_id: UUID, token: str) -> APIResponse[Loyalty]:
        url = f"/loyalty/{loyalty_id}"
        async with self.session.get(
            url,
            headers=get_auth_headers(token),
        ) as response:
            return await self._as_api_response(response, Loyalty)

    async def read_business_branches(
        self,
        business_id: UUID,
        token: str,
        limit: int = 10,
        offset: int = 0,
    ) -> APIResponse[BusinessBranchList]:
        url = f"/business/{business_id}/branch?limit={limit}&offset={offset}"
        async with self.session.get(
            url,
            headers=get_auth_headers(token),
        ) as response:
            return await self._as_api_response(response, BusinessBranchList)

    async def read_business_branch(
        self,
        business_branch_id: UUID,
        token: str,
    ) -> APIResponse[BusinessBranch]:
        url = f"/branch/{business_branch_id}"
        async with self.session.get(
            url,
            headers=get_auth_headers(token),
        ) as response:
            return await self._as_api_response(response, BusinessBranch)

    async def update_business_branch(
        self,
        business_branch_id: UUID,
        data: BusinessBranchForm,
        token: str,
    ) -> APIResponse[None]:
        url = f"/branch/{business_branch_id}"
        async with self.session.put(
            url,
            headers=get_auth_headers(token),
            json=data.model_dump(mode="json"),
        ) as response:
            return await self._as_api_response(response)

    async def update_loyalty(
        self,
        loyalty_id: UUID,
        data: LoyaltyForm,
        token: str,
    ) -> APIResponse[None]:
        url = f"/loyalty/{loyalty_id}"
        async with self.session.put(
            url,
            headers=get_auth_headers(token),
            json=data.model_dump(mode="json"),
        ) as response:
            return await self._as_api_response(response)

    async def delete_business_branch(
        self,
        business_branch_id: UUID,
        token: str,
    ) -> APIResponse[None]:
        url = f"/branch/{business_branch_id}"
        async with self.session.delete(
            url,
            headers=get_auth_headers(token),
        ) as response:
            return await self._as_api_response(response)
        
    async def delete_loyalty(
        self,
        loyalty_id: UUID,
        token: str,
    ) -> APIResponse[None]:
        url = f"/loyalty/{loyalty_id}"
        async with self.session.delete(
            url,
            headers=get_auth_headers(token),
        ) as response:
            return await self._as_api_response(response)

    async def logout(self, token: str) -> APIResponse[None]:
        url = "/user/logout"
        async with self.session.delete(
            url,
            headers=get_auth_headers(token),
        ) as response:
            return await self._as_api_response(response)
