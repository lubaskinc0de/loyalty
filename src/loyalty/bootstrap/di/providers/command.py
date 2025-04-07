from dishka import Provider, Scope, provide, provide_all

from loyalty.application.business.create_business import CreateBusiness
from loyalty.application.client.create_client import CreateClient
from loyalty.application.ping import Ping
from loyalty.presentation.web.controller.login import WebLogin


class CommandProvider(Provider):
    scope = Scope.REQUEST

    create_client = provide(CreateClient, scope=Scope.ACTION)
    create_business = provide(CreateBusiness, scope=Scope.ACTION)
    commands = provide_all(
        Ping,
        WebLogin,
    )
