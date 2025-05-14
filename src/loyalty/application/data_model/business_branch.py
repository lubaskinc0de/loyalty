from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from adaptix.conversion import get_converter
from pydantic import BaseModel, Field
from pydantic_extra_types.coordinate import Latitude, Longitude

from loyalty.application.shared_types import RussianPhoneNumber
from loyalty.domain.entity.business_branch import BusinessBranch


class BusinessBranchForm(BaseModel):
    name: str = Field(max_length=250, min_length=2)
    lon: Longitude
    lat: Latitude
    contact_phone: RussianPhoneNumber | None = None


@dataclass(slots=True, frozen=True)
class BusinessBranchData:
    business_branch_id: UUID
    name: str
    contact_phone: str | None
    location: str
    business_id: UUID
    created_at: datetime


convert_branch_to_dto = get_converter(BusinessBranch, BusinessBranchData)
convert_branches_to_dto = get_converter(Sequence[BusinessBranch], Sequence[BusinessBranchData])