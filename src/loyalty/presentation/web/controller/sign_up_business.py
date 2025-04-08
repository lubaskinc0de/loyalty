from dataclasses import dataclass

from dishka.container import ContextWrapper

from loyalty.adapters.auth.provider import WebUserCredentials
from loyalty.application.business.create_business import BusinessForm, CreateBusiness
from loyalty.domain.entity.user import User


class BusinessWebSignUpForm(WebUserCredentials):
    business_data: BusinessForm


@dataclass(slots=True, frozen=True)
class BusinessWebSignUp:
    container: ContextWrapper

    def execute(self, form: BusinessWebSignUpForm) -> User:
        with self.container as r_container, r_container(context={WebUserCredentials: form}) as action_container:
            interactor = action_container.get(CreateBusiness)
            client = interactor.execute(form.business_data)

        return client
