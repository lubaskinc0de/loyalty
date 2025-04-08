from dataclasses import dataclass

from dishka.container import ContextWrapper

from loyalty.adapters.auth.provider import WebUserCredentials
from loyalty.application.client.create_client import ClientForm, CreateClient
from loyalty.domain.entity.user import User


class ClientWebSignUpForm(WebUserCredentials):
    client_data: ClientForm


@dataclass(slots=True, frozen=True)
class ClientWebSignUp:
    container: ContextWrapper

    def execute(self, form: ClientWebSignUpForm) -> User:
        with self.container as r_container, r_container(context={WebUserCredentials: form}) as action_container:
            interactor = action_container.get(CreateClient)
            user = interactor.execute(form.client_data)

        return user
