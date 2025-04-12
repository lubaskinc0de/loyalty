from dataclasses import dataclass
from uuid import uuid4

from pydantic import BaseModel, Field
from pydantic_extra_types.coordinate import Latitude, Longitude

from loyalty.application.common.idp import BusinessIdProvider
from loyalty.application.common.uow import UoW
from loyalty.application.shared_types import RussianPhoneNumber
from loyalty.domain.entity.business_branch import BusinessBranch


class BusinessBranchForm(BaseModel):
    name: str = Field(max_length=250, min_length=2)
    address: str = Field(max_length=250, min_length=2)
    lon: Longitude
    lat: Latitude
    contact_phone: RussianPhoneNumber | None = None


@dataclass(slots=True, frozen=True)
class CreateBusinessBranch:
    uow: UoW
    idp: BusinessIdProvider

    def execute(self, form: BusinessBranchForm) -> None:
        business_branch_id = uuid4()

        location = f"POINT({float(form.lon)} {float(form.lat)})"
        business_branch = BusinessBranch(
            business_branch_id,
            name=form.name,
            address=form.address,
            contact_phone=form.contact_phone,
            location=location,
        )

        business = self.idp.get_business()

        self.uow.add(business_branch)
        self.uow.flush((business_branch,))
        business_branch.business = business
        self.uow.commit()
