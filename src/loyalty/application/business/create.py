from dataclasses import dataclass
from uuid import uuid4

from pydantic import BaseModel, EmailStr, Field
from pydantic_extra_types.coordinate import Latitude, Longitude

from loyalty.application.common.gateway.business import BusinessGateway
from loyalty.application.common.idp import UserIdProvider
from loyalty.application.common.uow import UoW
from loyalty.application.exceptions.business import BusinessAlreadyExistsError
from loyalty.application.shared_types import RussianPhoneNumber
from loyalty.domain.entity.business import Business
from loyalty.domain.entity.user import Role


class BusinessForm(BaseModel):
    name: str = Field(max_length=250, min_length=2)
    lon: Longitude
    lat: Latitude
    contact_phone: RussianPhoneNumber | None = None
    contact_email: EmailStr


@dataclass(slots=True, frozen=True)
class CreateBusiness:
    uow: UoW
    idp: UserIdProvider
    gateway: BusinessGateway

    def execute(self, form: BusinessForm) -> Business:
        user = self.idp.get_user()
        if Role.BUSINESS in user.available_roles:
            raise BusinessAlreadyExistsError

        business_id = uuid4()

        location = f"POINT({float(form.lon)} {float(form.lat)})"
        business = Business(
            business_id=business_id,
            name=form.name,
            contact_phone=form.contact_phone,
            contact_email=form.contact_email,
            location=location,
        )
        self.gateway.insert(business)

        user.business = business
        self.uow.commit()

        return business
