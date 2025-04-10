from dataclasses import dataclass
from uuid import UUID

from loyalty.application.common.gateway.business_branch import BusinessBranchGateway
from loyalty.application.common.idp import UserIdProvider
from loyalty.application.common.uow import UoW
from loyalty.application.exceptions.base import AccessDeniedError
from loyalty.application.exceptions.business_branch import BusinessBranchDoesNotExistsError
from loyalty.domain.entity.user import Role


@dataclass(slots=True, frozen=True)
class DeleteBusinessBranch:
    idp: UserIdProvider
    gateway: BusinessBranchGateway
    uow: UoW

    def execute(self, business_branch_id: UUID) -> None:
        user = self.idp.get_user()
        business_branch = self.gateway.get_by_id(business_branch_id)

        if any((Role.BUSINESS not in user.available_roles, business_branch.business != user.business)):
            raise AccessDeniedError
        if (business_branch := self.gateway.get_by_id(business_branch_id)) is None:
            raise BusinessBranchDoesNotExistsError

        self.uow.delete(business_branch)
        self.uow.commit()
