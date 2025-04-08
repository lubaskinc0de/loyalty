from dataclasses import dataclass

from dishka.container import ContextWrapper

from loyalty.adapters.auth.provider import WebUserCredentials
from loyalty.application.user.create import CreateUser
from loyalty.domain.entity.user import User


@dataclass(slots=True, frozen=True)
class WebSignUp:
    container: ContextWrapper

    def execute(self, form: WebUserCredentials) -> User:
        with self.container as r_container, r_container(context={WebUserCredentials: form}) as action_container:
            interactor = action_container.get(CreateUser)
            user = interactor.execute()

        return user
