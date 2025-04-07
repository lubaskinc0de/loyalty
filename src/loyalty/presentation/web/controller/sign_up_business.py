from dataclasses import dataclass

from dishka.container import ContextWrapper

from loyalty.adapters.hasher import Hasher
from loyalty.adapters.simple_auth import AuthUserId
from loyalty.application.business.create_business import BusinessForm, CreateBusiness
from loyalty.application.common.gateway.user_gateway import UserGateway
from loyalty.domain.entity.business import Business
from loyalty.presentation.web.controller.user import UserCredentials, create_user


class BusinessWebSignUpForm(UserCredentials):
    business_data: BusinessForm


@dataclass(slots=True, frozen=True)
class BusinessWebSignUp:
    container: ContextWrapper

    def execute(self, form: BusinessWebSignUpForm) -> Business:
        with self.container as r_container:
            hasher = r_container.get(Hasher)
            gateway = r_container.get(UserGateway)
            user = create_user(form, hasher, gateway)

            with r_container(context={AuthUserId: user.user_id}) as action_container:
                interactor = action_container.get(CreateBusiness)
                business = interactor.execute(form.business_data)

        return business
