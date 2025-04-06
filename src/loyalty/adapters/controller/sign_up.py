from dataclasses import dataclass
from uuid import uuid4

from dishka import Container
from pydantic import BaseModel, Field

from loyalty.adapters.idp import AuthUserId
from loyalty.application.common.gateway.user_gateway import UserGateway
from loyalty.application.common.hasher import Hasher
from loyalty.application.common.uow import UoW
from loyalty.application.create_client import ClientForm, CreateClient
from loyalty.domain.entity.client import Client
from loyalty.domain.entity.user import User


class SignUpForm(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=6, max_length=100)
    client_data: ClientForm


@dataclass(slots=True, frozen=True)
class SignUp:
    container: Container
    hasher: Hasher
    gateway: UserGateway
    uow: UoW

    def execute(self, form: SignUpForm) -> Client:
        hashed_password = self.hasher.hash(form.password)
        user_id = uuid4()
        user = User(user_id, form.username, hashed_password)
        self.gateway.insert(user)

        with self.container({AuthUserId: user_id}) as r_container:
            interactor = r_container.get(CreateClient)
            client = interactor.execute(form.client_data)

        return client
