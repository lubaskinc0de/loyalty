from dataclasses import dataclass
from uuid import UUID

from loyalty.application.common.gateway.business_branch import BusinessBranchGateway
from loyalty.application.common.idp import UserIdProvider
from loyalty.application.common.uow import UoW
from loyalty.application.exceptions.base import AccessDeniedError
from loyalty.application.exceptions.business_branch import BusinessBranchDoesNotExistError


@dataclass(slots=True, frozen=True)
class DeleteBusinessBranch:
    idp: UserIdProvider
    gateway: BusinessBranchGateway
    uow: UoW

    def execute(self, business_branch_id: UUID) -> None:
        user = self.idp.get_user()
        business_branch = self.gateway.get_by_id(business_branch_id)

        if business_branch is None:
            raise BusinessBranchDoesNotExistError

        if not business_branch.can_edit(user):
            raise AccessDeniedError

        self.uow.delete(business_branch)
        self.uow.commit()
