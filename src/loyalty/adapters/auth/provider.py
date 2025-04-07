from dataclasses import dataclass

from loyalty.adapters.auth.user import WebUser
from loyalty.application.common.auth_provider import AuthProvider
from loyalty.domain.entity.business import Business
from loyalty.domain.entity.client import Client


@dataclass(slots=True, frozen=True)
class WebAuthProvider(AuthProvider):
    user: WebUser

    def bind_client_to_auth(self, client: Client) -> None:
        self.user.client = client

    def bind_business_to_auth(self, business: Business) -> None:
        self.user.business = business
