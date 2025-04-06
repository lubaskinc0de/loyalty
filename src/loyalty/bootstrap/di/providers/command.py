from dishka import Provider, Scope, provide_all

from loyalty.adapters.controller.sign_up import SignUp
from loyalty.application.create_client import CreateClient
from loyalty.application.ping import Ping


class CommandProvider(Provider):
    scope = Scope.REQUEST

    commands = provide_all(
        Ping,
        CreateClient,
        SignUp,
    )
