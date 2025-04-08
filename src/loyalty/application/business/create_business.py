from dataclasses import dataclass
from uuid import uuid4

from pydantic import BaseModel, EmailStr, Field
from pydantic_extra_types.coordinate import Latitude, Longitude

from loyalty.application.common.auth_provider import AuthProvider
from loyalty.application.common.gateway.business import BusinessGateway
from loyalty.application.common.uow import UoW
from loyalty.application.shared_types import RussianPhoneNumber
from loyalty.domain.entity.business import Business
from loyalty.domain.entity.user import User


class BusinessForm(BaseModel):
    name: str = Field(max_length=250, min_length=2)
    lon: Longitude
    lat: Latitude
    contact_phone: RussianPhoneNumber | None = None
    contact_email: EmailStr


@dataclass(slots=True, frozen=True)
class CreateBusiness:
    uow: UoW
    auth: AuthProvider
    gateway: BusinessGateway

    def execute(self, form: BusinessForm) -> User:
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

        user = User(
            user_id=uuid4(),
            business=business,
        )
        self.uow.add(user)
        self.uow.flush((user,))

        self.auth.bind_to_auth(user)
        self.uow.commit()

        return user
