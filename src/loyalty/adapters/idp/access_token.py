from dataclasses import dataclass
from typing import Literal
from uuid import UUID


@dataclass(slots=True, frozen=True)
class AccessToken:
    role: Literal["client", "business"]
    entity_id: UUID
