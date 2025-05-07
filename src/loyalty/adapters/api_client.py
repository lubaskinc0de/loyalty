from dataclasses import dataclass, field
from typing import Literal, TypeVar
from uuid import UUID

from adaptix import Retort
from aiohttp import ClientResponse, ClientSession

from loyalty.adapters.api_models import BusinessBranchId, LoyaltyId, MembershipId
from loyalty.adapters.auth.provider import WebUserCredentials
from loyalty.application.business.create import BusinessForm
from loyalty.application.business_branch.dto import BusinessBranches
from loyalty.application.client.create import ClientForm
from loyalty.application.data_model.business_branch import BusinessBranchForm
from loyalty.application.loyalty.create import LoyaltyForm
from loyalty.application.loyalty.dto import Loyalties
from loyalty.application.loyalty.update import UpdateLoyaltyForm
from loyalty.application.membership.create import MembershipForm
from loyalty.domain.entity.business import Business
from loyalty.domain.entity.business_branch import BusinessBranch
from loyalty.domain.entity.client import Client
from loyalty.domain.entity.loyalty import Loyalty
from loyalty.domain.entity.membership import LoyaltyMembership
from loyalty.domain.entity.user import User
from loyalty.domain.shared_types import LoyaltyTimeFrame
from loyalty.presentation.web.controller.login import TokenResponse

retort = Retort()
T = TypeVar("T")


class CannotUnwrapError(Exception): ...


class StatusMismatchError(Exception): ...


def get_auth_headers(token: str | None = None) -> dict[str, str]:
    if token is None:
        return {}
    return {"Authorization": f"Bearer {token}"}


@dataclass(slots=True, frozen=True)
class PingResponse:
    ping: Literal["pong"]


@dataclass(slots=True, frozen=True)
class APIResponse[T]:
    content: T | None
    http_response: ClientResponse
    error: dict[str, str] | None

    def unwrap(self) -> T:
        if self.content is None:
            raise CannotUnwrapError
        return self.content

    def except_status(self, status: int) -> None:
        if self.http_response.status != status:
            raise StatusMismatchError


@dataclass(slots=True)
class LoyaltyClient:
    session: ClientSession
    token: str | None = field(default=None, init=False, repr=False)

    def authorize(self, token: str) -> None:
        self.token = token

    def reset_authorization(self) -> None:
        self.token = None

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

    async def create_client(self, data: ClientForm) -> APIResponse[None]:
        url = "/client/"
        async with self.session.post(
            url,
            json=data.model_dump(mode="json"),
            headers=get_auth_headers(self.token),
        ) as response:
            return await self._as_api_response(response)

    async def create_business(self, data: BusinessForm) -> APIResponse[None]:
        url = "/business/"
        async with self.session.post(
            url,
            json=data.model_dump(mode="json"),
            headers=get_auth_headers(self.token),
        ) as response:
            return await self._as_api_response(response)

    async def create_business_branch(
        self,
        data: BusinessBranchForm,
    ) -> APIResponse[BusinessBranchId]:
        url = "/branch"
        async with self.session.post(
            url,
            json=data.model_dump(mode="json"),
            headers=get_auth_headers(self.token),
        ) as response:
            return await self._as_api_response(response, BusinessBranchId)

    async def create_loyalty(
        self,
        data: LoyaltyForm,
    ) -> APIResponse[LoyaltyId]:
        url = "/loyalty"
        async with self.session.post(
            url,
            json=data.model_dump(mode="json"),
            headers=get_auth_headers(self.token),
        ) as response:
            return await self._as_api_response(response, LoyaltyId)

    async def login(self, data: WebUserCredentials) -> APIResponse[TokenResponse]:
        url = "/user/login"
        async with self.session.post(url, json=data.model_dump(mode="json")) as response:
            return await self._as_api_response(response, TokenResponse)

    async def read_client(self) -> APIResponse[Client]:
        url = "/client/"
        async with self.session.get(
            url,
            headers=get_auth_headers(self.token),
        ) as response:
            return await self._as_api_response(response, Client)

    async def read_user(self) -> APIResponse[User]:
        url = "/user/"
        async with self.session.get(
            url,
            headers=get_auth_headers(self.token),
        ) as response:
            return await self._as_api_response(response, User)

    async def read_business(self, business_id: UUID) -> APIResponse[Business]:
        url = f"/business/{business_id}"
        async with self.session.get(
            url,
            headers=get_auth_headers(self.token),
        ) as response:
            return await self._as_api_response(response, Business)

    async def read_loyalty(self, loyalty_id: UUID) -> APIResponse[Loyalty]:
        url = f"/loyalty/{loyalty_id}"
        async with self.session.get(
            url,
            headers=get_auth_headers(self.token),
        ) as response:
            return await self._as_api_response(response, Loyalty)

    async def read_loyalties(
        self,
        time_frame: LoyaltyTimeFrame = LoyaltyTimeFrame.CURRENT,
        business_id: UUID | None = None,
        active: bool | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> APIResponse[Loyalties]:
        url = f"/loyalty/?limit={limit}&offset={offset}&time_frame={time_frame.value}"

        if active is not None:
            int_active: int = 1 if active is True else 0
            url += f"&active={int_active}"

        if business_id:
            url += f"&business_id={business_id}"

        async with self.session.get(
            url,
            headers=get_auth_headers(self.token),
        ) as response:
            return await self._as_api_response(response, Loyalties)

    async def read_business_branches(
        self,
        business_id: UUID,
        limit: int = 10,
        offset: int = 0,
    ) -> APIResponse[BusinessBranches]:
        url = f"/business/{business_id}/branch?limit={limit}&offset={offset}"
        async with self.session.get(
            url,
            headers=get_auth_headers(self.token),
        ) as response:
            return await self._as_api_response(response, BusinessBranches)

    async def read_business_branch(
        self,
        business_branch_id: UUID,
    ) -> APIResponse[BusinessBranch]:
        url = f"/branch/{business_branch_id}"
        async with self.session.get(
            url,
            headers=get_auth_headers(self.token),
        ) as response:
            return await self._as_api_response(response, BusinessBranch)

    async def update_business_branch(
        self,
        business_branch_id: UUID,
        data: BusinessBranchForm,
    ) -> APIResponse[None]:
        url = f"/branch/{business_branch_id}"
        async with self.session.put(
            url,
            headers=get_auth_headers(self.token),
            json=data.model_dump(mode="json"),
        ) as response:
            return await self._as_api_response(response)

    async def update_loyalty(
        self,
        loyalty_id: UUID,
        data: UpdateLoyaltyForm,
    ) -> APIResponse[None]:
        url = f"/loyalty/{loyalty_id}"
        async with self.session.put(
            url,
            headers=get_auth_headers(self.token),
            json=data.model_dump(mode="json"),
        ) as response:
            return await self._as_api_response(response)

    async def delete_business_branch(
        self,
        business_branch_id: UUID,
    ) -> APIResponse[None]:
        url = f"/branch/{business_branch_id}"
        async with self.session.delete(
            url,
            headers=get_auth_headers(self.token),
        ) as response:
            return await self._as_api_response(response)

    async def delete_loyalty(
        self,
        loyalty_id: UUID,
    ) -> APIResponse[None]:
        url = f"/loyalty/{loyalty_id}"
        async with self.session.delete(
            url,
            headers=get_auth_headers(self.token),
        ) as response:
            return await self._as_api_response(response)

    async def logout(self) -> APIResponse[None]:
        url = "/user/logout"
        async with self.session.delete(
            url,
            headers=get_auth_headers(self.token),
        ) as response:
            return await self._as_api_response(response)

    async def create_membership(
        self,
        data: MembershipForm,
    ) -> APIResponse[MembershipId]:
        url = "/membership"
        async with self.session.post(
            url,
            json=data.model_dump(mode="json"),
            headers=get_auth_headers(self.token),
        ) as response:
            return await self._as_api_response(response, MembershipId)

    async def delete_membership(
        self,
        membership_id: UUID,
    ) -> APIResponse[None]:
        url = f"/membership/{membership_id}"
        async with self.session.delete(
            url,
            headers=get_auth_headers(self.token),
        ) as response:
            return await self._as_api_response(response)

    async def read_membership(
        self,
    ) -> APIResponse[LoyaltyMembership]:
        url = "/client/membership/"
        async with self.session.get(
            url,
            headers=get_auth_headers(self.token),
        ) as response:
            return await self._as_api_response(response, LoyaltyMembership)
