from dataclasses import dataclass
from uuid import UUID

from dishka.container import ContextWrapper

from loyalty.adapters.auth.hasher import Hasher
from loyalty.adapters.auth.user import WebUser
from loyalty.adapters.common.user_gateway import WebUserGateway
from loyalty.application.client.create_client import ClientForm, CreateClient
from loyalty.domain.entity.client import Client
from loyalty.presentation.web.controller.user import WebUserCredentials, create_user


class ClientWebSignUpForm(WebUserCredentials):
    client_data: ClientForm


@dataclass(slots=True)
class CreatedClient:
    client: Client
    user_id: UUID


@dataclass(slots=True, frozen=True)
class ClientWebSignUp:
    container: ContextWrapper

    def execute(self, form: ClientWebSignUpForm) -> CreatedClient:
        with self.container as r_container:
            hasher = r_container.get(Hasher)
            gateway = r_container.get(WebUserGateway)
            user = create_user(form, hasher, gateway)

            with r_container(context={WebUser: user}) as action_container:
                interactor = action_container.get(CreateClient)
                client = interactor.execute(form.client_data)

        return CreatedClient(client=client, user_id=user.user_id)
