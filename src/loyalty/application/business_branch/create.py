from dataclasses import dataclass
from uuid import UUID, uuid4

from loyalty.application.common.idp import BusinessIdProvider
from loyalty.application.common.uow import UoW
from loyalty.application.data_model.business_branch import BusinessBranchForm
from loyalty.domain.entity.business_branch import BusinessBranch


@dataclass(slots=True, frozen=True)
class CreateBusinessBranch:
    uow: UoW
    idp: BusinessIdProvider

    def execute(self, form: BusinessBranchForm) -> UUID:
        business = self.idp.get_business()
        business_branch_id = uuid4()
        location = f"POINT({float(form.lon)} {float(form.lat)})"
        business_branch = BusinessBranch(
            business_branch_id,
            name=form.name,
            contact_phone=form.contact_phone,
            location=location,
            business=business,
        )
        self.uow.add(business_branch)
        self.uow.commit()

        return business_branch.business_branch_id
