from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, frozen=True)
class AccessToken:
    user_id: UUID
    token: str
