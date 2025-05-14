from dataclasses import dataclass
from decimal import Decimal

from loyalty.application.common.gateway.business import BusinessGateway
from loyalty.application.common.idp import BusinessIdProvider


@dataclass(slots=True, frozen=True)
class BusinessStats:
    payments_amount: Decimal
    waste_amount: Decimal
    bonus_given_amount: Decimal
    loyalties_count: int
    memberships_count: int


@dataclass(slots=True, frozen=True)
class ReadBusinessStats:
    idp: BusinessIdProvider
    gateway: BusinessGateway

    def execute(self) -> BusinessStats:
        business = self.idp.get_business()
        payments_stats = self.gateway.get_business_payments_stat(business.business_id)
        loyalties_count = self.gateway.get_business_loyalties_count(business.business_id)
        memberships_count = self.gateway.get_business_memberships_count(business.business_id)

        return BusinessStats(
            payments_amount=payments_stats.payments_amount,
            waste_amount=payments_stats.waste_amount,
            bonus_given_amount=payments_stats.bonus_given_amount,
            loyalties_count=loyalties_count,
            memberships_count=memberships_count,
        )
