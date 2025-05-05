from dataclasses import dataclass
from uuid import uuid4

from pydantic import BaseModel, Field
from pydantic_extra_types.coordinate import Latitude, Longitude

from loyalty.application.common.idp import UserIdProvider
from loyalty.application.common.uow import UoW
from loyalty.application.exceptions.client import ClientAlreadyExistsError
from loyalty.application.shared_types import RussianPhoneNumber
from loyalty.domain.entity.client import Client
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
    idp: UserIdProvider

    def execute(self, form: ClientForm) -> None:
        user = self.idp.get_user()

        if not user.can_create_client():
            raise ClientAlreadyExistsError

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
        user.client = client
        self.uow.commit()
