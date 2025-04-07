from dataclasses import dataclass

from dishka.container import ContextWrapper

from loyalty.adapters.hasher import Hasher
from loyalty.adapters.simple_auth import AuthUserId
from loyalty.application.client.create_client import ClientForm, CreateClient
from loyalty.application.common.gateway.user_gateway import UserGateway
from loyalty.domain.entity.client import Client
from loyalty.presentation.web.controller.user import UserCredentials, create_user


class ClientWebSignUpForm(UserCredentials):
    client_data: ClientForm


@dataclass(slots=True, frozen=True)
class ClientWebSignUp:
    container: ContextWrapper

    def execute(self, form: ClientWebSignUpForm) -> Client:
        with self.container as r_container:
            hasher = r_container.get(Hasher)
            gateway = r_container.get(UserGateway)
            user = create_user(form, hasher, gateway)

            with r_container(context={AuthUserId: user.user_id}) as action_container:
                interactor = action_container.get(CreateClient)
                client = interactor.execute(form.client_data)

        return client
