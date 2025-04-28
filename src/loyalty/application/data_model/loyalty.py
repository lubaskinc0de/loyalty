from dataclasses import Field
from datetime import datetime
from pydantic import BaseModel

from loyalty.domain.shared_types import Gender


class LoyaltyForm(BaseModel):
    name: str = Field(max_length=100, min_length=2)
    description: str = Field(max_length=3096)
    starts_at: datetime
    ends_at: datetime
    money_per_bonus: int
    min_age: int
    max_age: int
    is_active: bool
    gender: Gender | None = None