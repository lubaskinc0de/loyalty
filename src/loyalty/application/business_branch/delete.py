from dataclasses import dataclass
from uuid import UUID

from loyalty.application.common.gateway.business_branch import BusinessBranchGateway
from loyalty.application.common.idp import BusinessIdProvider
from loyalty.application.common.uow import UoW
from loyalty.application.exceptions.base import AccessDeniedError
from loyalty.application.exceptions.business_branch import BusinessBranchDoesNotExistError


@dataclass(slots=True, frozen=True)
class DeleteBusinessBranch:
    idp: BusinessIdProvider
    gateway: BusinessBranchGateway
    uow: UoW

    def execute(self, business_branch_id: UUID) -> None:
        business_branch = self.gateway.get_by_id(business_branch_id)

        if business_branch is None:
            raise BusinessBranchDoesNotExistError

        business = self.idp.get_business()

        if business_branch.business != business:
            raise AccessDeniedError

        self.uow.delete(business_branch)
        self.uow.commit()
