from pydantic import BaseModel, Field
from pydantic_extra_types.coordinate import Latitude, Longitude

from loyalty.application.shared_types import RussianPhoneNumber


class BusinessBranchForm(BaseModel):
    name: str = Field(max_length=250, min_length=2)
    lon: Longitude
    lat: Latitude
    contact_phone: RussianPhoneNumber | None = None
