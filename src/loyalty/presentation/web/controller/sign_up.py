from dataclasses import dataclass
from uuid import uuid4

from dishka.container import ContextWrapper
from pydantic import BaseModel, Field

from loyalty.adapters.hasher import Hasher
from loyalty.adapters.idp import AuthUserId
from loyalty.application.common.gateway.user_gateway import UserGateway
from loyalty.application.create_client import ClientForm, CreateClient
from loyalty.domain.entity.client import Client
from loyalty.domain.entity.user import User


class ClientWebSignUpForm(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=6, max_length=100)
    client_data: ClientForm


@dataclass(slots=True, frozen=True)
class ClientWebSignUp:
    container: ContextWrapper

    def execute(self, form: ClientWebSignUpForm) -> Client:
        with self.container as r_container:
            hasher = r_container.get(Hasher)
            gateway = r_container.get(UserGateway)

            hashed_password = hasher.hash(form.password)
            user_id = uuid4()
            user = User(user_id, form.username, hashed_password)
            gateway.insert(user)

            with r_container(context={AuthUserId: user_id}) as action_container:
                interactor = action_container.get(CreateClient)
                client = interactor.execute(form.client_data)

        return client
