from dishka import Provider, Scope, provide_all

from crudik.application.ping import Ping


class CommandProvider(Provider):
    scope = Scope.REQUEST

    commands = provide_all(
        Ping,
    )
