from dishka import Provider, Scope, provide, provide_all

from loyalty.application.create_client import CreateClient
from loyalty.application.ping import Ping


class CommandProvider(Provider):
    scope = Scope.REQUEST

    create_client = provide(CreateClient, scope=Scope.ACTION)
    commands = provide_all(
        Ping,
    )
