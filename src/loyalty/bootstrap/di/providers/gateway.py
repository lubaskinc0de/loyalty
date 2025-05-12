from dishka import Provider, Scope, WithParents, provide_all

from loyalty.adapters.db.gateway.bonus import SABonusGateway
from loyalty.adapters.db.gateway.business import SABusinessGateway
from loyalty.adapters.db.gateway.business_branch import SABusinessBranchGateway
from loyalty.adapters.db.gateway.client import SAClientGateway
from loyalty.adapters.db.gateway.loyalty import SALoyaltyGateway
from loyalty.adapters.db.gateway.membership import SAMembershipGateway
from loyalty.adapters.db.gateway.user import AuthGateway


class GatewayProvider(Provider):
    scope = Scope.REQUEST
    gateways = provide_all(
        WithParents[AuthGateway],  # type: ignore
        WithParents[SABusinessGateway],  # type: ignore
        WithParents[SAClientGateway],  # type:ignore
        WithParents[SABusinessBranchGateway],  # type:ignore
        WithParents[SALoyaltyGateway],  # type:ignore
        WithParents[SAMembershipGateway],  # type: ignore
        WithParents[SABonusGateway],  # type: ignore
    )
