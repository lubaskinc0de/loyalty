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
    gateway: BusinessBranchGateway

    def execute(self, business_branch_id: UUID) -> BusinessBranch:
        user = self.idp.get_user()
        if not user.is_one_of(Role.CLIENT, Role.BUSINESS):
            raise AccessDeniedError
        if (business_branch := self.gateway.get_by_id(business_branch_id)) is None:
            raise BusinessBranchDoesNotExistError
        return business_branch


@dataclass(slots=True, frozen=True)
class ReadBusinessBranches:
    idp: UserIdProvider
    gateway: BusinessBranchGateway

    def execute(self, business_id: UUID, limit: int, offset: int) -> BusinessBranches:
        user = self.idp.get_user()
        if not user.is_one_of(Role.CLIENT, Role.BUSINESS):
            raise AccessDeniedError

        business_branches = self.gateway.get_business_branches(
            limit=limit,
            offset=offset,
            business_id=business_id,
        )
        return business_branches
