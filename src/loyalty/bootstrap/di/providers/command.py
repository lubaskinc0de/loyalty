from dishka import Provider, Scope, provide, provide_all

from loyalty.application.business.create_business import CreateBusiness
from loyalty.application.client.create_client import CreateClient
from loyalty.application.client.read_client import ReadClient
from loyalty.application.ping import Ping
from loyalty.application.user.create_user import CreateUser
from loyalty.presentation.web.controller.login import WebLogin


class CommandProvider(Provider):
    scope = Scope.REQUEST

    create_user = provide(CreateUser, scope=Scope.ACTION)
    commands = provide_all(
        Ping,
        WebLogin,
        ReadClient,
        CreateClient,
        CreateBusiness,
    )
