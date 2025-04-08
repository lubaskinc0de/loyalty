from dataclasses import dataclass
from uuid import uuid4

from pydantic import BaseModel, Field
from pydantic_extra_types.coordinate import Latitude, Longitude

from loyalty.application.common.auth_provider import AuthProvider
from loyalty.application.common.uow import UoW
from loyalty.application.shared_types import RussianPhoneNumber
from loyalty.domain.entity.client import Client
from loyalty.domain.entity.user import User
from loyalty.domain.shared_types import Gender


class ClientForm(BaseModel):
    full_name: str = Field(max_length=250, min_length=4)
    age: int = Field(ge=0, le=100)
    lon: Longitude
    lat: Latitude
    gender: Gender
    phone: RussianPhoneNumber


@dataclass(slots=True, frozen=True)
class CreateClient:
    uow: UoW
    auth: AuthProvider

    def execute(self, form: ClientForm) -> User:
        client_id = uuid4()

        location = f"POINT({float(form.lon)} {float(form.lat)})"
        client = Client(
            client_id,
            form.full_name,
            form.age,
            form.gender,
            str(form.phone),
            location,
        )
        self.uow.add(client)
        self.uow.flush((client,))

        user = User(
            user_id=uuid4(),
            client=client,
        )
        self.uow.add(user)
        self.uow.flush((user,))

        self.auth.bind_to_auth(user)
        self.uow.commit()

        return user
