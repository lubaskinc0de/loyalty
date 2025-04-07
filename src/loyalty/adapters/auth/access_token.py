from dataclasses import dataclass
from uuid import UUID

from loyalty.adapters.auth.user import WebUser


@dataclass
class AccessToken:
    user_id: UUID
    token: str
    user: WebUser
