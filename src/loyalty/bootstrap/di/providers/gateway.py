from dishka import Provider, Scope, WithParents, provide_all

from loyalty.adapters.db.gateway.bonus import SABonusGateway
from loyalty.adapters.db.gateway.business import SABusinessGateway
from loyalty.adapters.db.gateway.business_branch import SABusinessBranchGateway
from loyalty.adapters.db.gateway.client import SAClientGateway
from loyalty.adapters.db.gateway.loyalty import SALoyaltyGateway
from loyalty.adapters.db.gateway.membership import SAMembershipGateway
from loyalty.adapters.db.gateway.payment import SAPaymentGateway
from loyalty.adapters.db.gateway.statistic import SAStatisticsGateway
from loyalty.adapters.db.gateway.user import AuthGateway


class GatewayProvider(Provider):
    scope = Scope.REQUEST
    gateways = provide_all(
        WithParents[AuthGateway],
        WithParents[SABusinessGateway],
        WithParents[SAClientGateway],
        WithParents[SABusinessBranchGateway],
        WithParents[SALoyaltyGateway],
        WithParents[SAMembershipGateway],
        WithParents[SABonusGateway],
        WithParents[SAPaymentGateway],
        WithParents[SAStatisticsGateway],
    )
