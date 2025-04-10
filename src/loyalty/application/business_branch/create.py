from dataclasses import dataclass
from uuid import uuid4

from pydantic import BaseModel, EmailStr, Field
from pydantic_extra_types.coordinate import Latitude, Longitude

from loyalty.application.common.idp import UserIdProvider
from loyalty.application.common.uow import UoW
from loyalty.application.exceptions.base import AccessDeniedError
from loyalty.application.shared_types import RussianPhoneNumber
from loyalty.domain.entity.business_branch import BusinessBranch
from loyalty.domain.entity.user import Role


class BusinessBranchForm(BaseModel):
    name: str = Field(max_length=250, min_length=2)
    address: str = Field(max_length=250, min_length=2)
    lon: Longitude
    lat: Latitude
    contact_phone: RussianPhoneNumber | None = None
    contact_email: EmailStr


@dataclass(slots=True, frozen=True)
class CreateBusinessBranch:
    uow: UoW
    idp: UserIdProvider

    def execute(self, form: BusinessBranchForm) -> None:
        user = self.idp.get_user()

        if Role.BUSINESS not in user.available_roles:
            raise AccessDeniedError

        business_branch_id = uuid4()

        location = f"POINT({float(form.lon)} {float(form.lat)})"
        business_branch = BusinessBranch(
            business_branch_id,
            name=form.name,
            address=form.address,
            contact_email=form.contact_email,
            contact_phone=form.contact_phone,
            location=location,
        )

        self.uow.add(business_branch)
        self.uow.flush((business_branch,))
        business_branch.business = user.business
        self.uow.commit()
