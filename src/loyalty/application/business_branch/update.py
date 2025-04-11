from dataclasses import dataclass
from uuid import UUID

from loyalty.application.business_branch.create import BusinessBranchForm
from loyalty.application.common.gateway.business_branch import BusinessBranchGateway
from loyalty.application.common.idp import UserIdProvider
from loyalty.application.common.uow import UoW
from loyalty.application.exceptions.base import AccessDeniedError
from loyalty.application.exceptions.business_branch import BusinessBranchDoesNotExistError
from loyalty.domain.entity.user import Role


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

        if any((Role.BUSINESS not in user.available_roles, business_branch.business != user.business)):
            raise AccessDeniedError

        business_branch.name = form.name or business_branch.name
        business_branch.address = form.address or business_branch.address
        business_branch.contact_email = form.contact_email or business_branch.contact_email
        business_branch.contact_phone = form.contact_phone or business_branch.contact_phone

        if form.lon and form.lat:
            business_branch.location = f"POINT({float(form.lon)} {float(form.lat)})"

        self.uow.add(business_branch)

        self.uow.commit()
