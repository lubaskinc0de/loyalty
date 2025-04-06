from dishka import Provider, Scope, provide

from loyalty.adapters.db.gateway.user import SAUserGateway
from loyalty.application.common.gateway.user_gateway import UserGateway


class GatewayProvider(Provider):
    scope = Scope.REQUEST
    user_gateway = provide(SAUserGateway, provides=UserGateway)
