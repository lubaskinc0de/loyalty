from dataclasses import dataclass
from uuid import uuid4

from pydantic import BaseModel, Field

from loyalty.adapters.auth.hasher import Hasher
from loyalty.adapters.auth.user import WebUser
from loyalty.adapters.common.gateway import WebUserGateway
from loyalty.application.common.auth_provider import AuthProvider
from loyalty.domain.entity.user import User


class WebUserCredentials(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=6, max_length=100)


@dataclass(slots=True, frozen=True)
class WebAuthProvider(AuthProvider):
    hasher: Hasher
    gateway: WebUserGateway
    form: WebUserCredentials

    def bind_to_auth(self, user: User) -> None:
        hashed_password = self.hasher.hash(self.form.password)
        web_user_id = uuid4()
        web_user = WebUser(web_user_id, self.form.username, hashed_password, user)
        self.gateway.insert(web_user)
