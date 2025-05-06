from dataclasses import dataclass
from uuid import UUID

from loyalty.application.business_branch.dto import BusinessBranches
from loyalty.application.common.gateway.business_branch import BusinessBranchGateway
from loyalty.application.common.idp import UserIdProvider
from loyalty.application.exceptions.base import AccessDeniedError
from loyalty.application.exceptions.business_branch import BusinessBranchDoesNotExistError
from loyalty.domain.entity.business_branch import BusinessBranch


@dataclass(slots=True, frozen=True)
class ReadBusinessBranch:
    idp: UserIdProvider
    gateway: BusinessBranchGateway

    def execute(self, business_branch_id: UUID) -> BusinessBranch:
        user = self.idp.get_user()
        if (business_branch := self.gateway.get_by_id(business_branch_id)) is None:
            raise BusinessBranchDoesNotExistError

        if not business_branch.can_read(user):
            raise AccessDeniedError

        return business_branch


@dataclass(slots=True, frozen=True)
class ReadBusinessBranches:
    idp: UserIdProvider
    gateway: BusinessBranchGateway

    def execute(self, business_id: UUID, limit: int, offset: int) -> BusinessBranches:
        user = self.idp.get_user()
        if not BusinessBranch.can_read_list(user):
            raise AccessDeniedError

        business_branches = self.gateway.get_business_branches(
            limit=limit,
            offset=offset,
            business_id=business_id,
        )
        return business_branches
