from dataclasses import dataclass
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic_extra_types.coordinate import Latitude, Longitude

from loyalty.application.common.gateway.business_branch import BusinessBranchGateway
from loyalty.application.common.idp import BusinessIdProvider
from loyalty.application.common.uow import UoW
from loyalty.application.exceptions.base import AccessDeniedError
from loyalty.application.exceptions.business_branch import BusinessBranchDoesNotExistError
from loyalty.application.shared_types import RussianPhoneNumber


class UpdatedBusinessBranchForm(BaseModel):
    name: str = Field(max_length=250, min_length=2)
    address: str = Field(max_length=250, min_length=2)
    lon: Longitude
    lat: Latitude
    contact_phone: RussianPhoneNumber


@dataclass(slots=True, frozen=True)
class UpdateBusinessBranch:
    uow: UoW
    idp: BusinessIdProvider
    gateway: BusinessBranchGateway

    def execute(self, business_branch_id: UUID, form: UpdatedBusinessBranchForm) -> None:
        business_branch = self.gateway.get_by_id(business_branch_id)

        if business_branch is None:
            raise BusinessBranchDoesNotExistError

        business = self.idp.get_business()

        if business_branch.business != business:
            raise AccessDeniedError

        business_branch.name = form.name
        business_branch.address = form.address
        business_branch.contact_phone = form.contact_phone
        business_branch.location = f"POINT({float(form.lon)} {float(form.lat)})"

        self.uow.add(business_branch)

        self.uow.commit()
