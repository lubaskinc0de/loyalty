from dataclasses import dataclass
from uuid import UUID

from loyalty.domain.entity.user import User


@dataclass
class AccessToken:
    user_id: UUID
    token: str
    user: User
