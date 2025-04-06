from dataclasses import dataclass
from uuid import uuid4

from pydantic import BaseModel, Field
from pydantic_extra_types.phone_numbers import PhoneNumber

from loyalty.application.common.geo_finder import GeoFinder
from loyalty.application.common.idp import IdProvider
from loyalty.application.common.uow import UoW
from loyalty.application.exceptions.client import ClientCityDoesNotExistsError
from loyalty.domain.entity.client import Client
from loyalty.domain.shared_types import Gender

PhoneNumber.supported_regions = ["ru"]


class ClientForm(BaseModel):
    full_name: str = Field(max_length=250, min_length=4)
    age: int = Field(ge=0, le=100)
    city: str = Field(max_length=150)
    gender: Gender
    phone: PhoneNumber


@dataclass(slots=True, frozen=True)
class CreateClient:
    uow: UoW
    idp: IdProvider
    geo_finder: GeoFinder

    def execute(self, form: ClientForm) -> Client:
        client_city = self.geo_finder.find_city(form.city)
        if client_city is None:
            raise ClientCityDoesNotExistsError
        client_id = uuid4()

        client = Client(client_id, form.full_name, form.age, form.city, form.gender, str(form.phone))
        self.uow.flush((client,))
        self.idp.bind_client_auth(client_id)
        self.uow.commit()

        return client
