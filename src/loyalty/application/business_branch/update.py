from dataclasses import dataclass
from uuid import UUID

from loyalty.application.common.gateway.business_branch import BusinessBranchGateway
from loyalty.application.common.idp import UserIdProvider
from loyalty.application.common.uow import UoW
from loyalty.application.data_model.business_branch import BusinessBranchForm
from loyalty.application.exceptions.base import AccessDeniedError
from loyalty.application.exceptions.business_branch import BusinessBranchDoesNotExistError


@dataclass(slots=True, frozen=True)
class UpdateBusinessBranch:
    uow: UoW
    idp: UserIdProvider
    gateway: BusinessBranchGateway

    def execute(self, business_branch_id: UUID, form: BusinessBranchForm) -> None:
        user = self.idp.get_user()
        business_branch = self.gateway.get_by_id(business_branch_id)
        if business_branch is None:
            raise BusinessBranchDoesNotExistError

        if not business_branch.can_edit(user):
            raise AccessDeniedError

        business_branch.name = form.name
        business_branch.contact_phone = form.contact_phone
        business_branch.location = f"POINT({form.lon!s} {form.lat!s})"

        self.uow.add(business_branch)

        self.uow.commit()
