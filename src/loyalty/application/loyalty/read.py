from dataclasses import dataclass
from uuid import UUID, uuid4

from loyalty.application.common.gateway.loyalty import LoyaltyGateway
from loyalty.application.common.idp import BusinessIdProvider
from loyalty.application.common.uow import UoW
from loyalty.application.data_model.loyalty import LoyaltyForm
from loyalty.application.exceptions.loyalty import LoyaltyDoesNotExistError
from loyalty.domain.entity.loyalty import Loyalty


from dataclasses import dataclass
from uuid import UUID

from loyalty.application.business_branch.dto import BusinessBranches
from loyalty.application.common.gateway.business_branch import BusinessBranchGateway
from loyalty.application.common.idp import UserIdProvider
from loyalty.application.exceptions.base import AccessDeniedError
from loyalty.application.exceptions.business_branch import BusinessBranchDoesNotExistError
from loyalty.domain.entity.business_branch import BusinessBranch
from loyalty.domain.entity.user import Role


@dataclass(slots=True, frozen=True)
class ReadBusinessBranch:
    idp: UserIdProvider
    gateway: LoyaltyGateway

    def execute(self, loyalty_id: UUID) -> Loyalty:
        user = self.idp.get_user()
        
        if not user.is_one_of(Role.CLIENT, Role.BUSINESS):
            raise AccessDeniedError
        if (loyalty := self.gateway.get_by_id(loyalty_id)) is None:
            raise LoyaltyDoesNotExistError
        
        return loyalty