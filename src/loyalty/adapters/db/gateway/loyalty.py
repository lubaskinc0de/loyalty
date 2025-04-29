from dataclasses import dataclass
from uuid import UUID

from sqlalchemy.orm import Session

from loyalty.application.common.gateway.loyalty import LoyaltyGateway
from loyalty.domain.entity.business_branch import BusinessBranch
from loyalty.domain.entity.loyalty import Loyalty


@dataclass(slots=True, frozen=True)
class SALoyaltyGateway(LoyaltyGateway):
    session: Session

    def get_by_id(self, loyalty_id: UUID) -> Loyalty | None:
        return self.session.get(BusinessBranch, loyalty_id)
