from dataclasses import dataclass
from uuid import UUID

from loyalty.domain.shared_types import Gender


@dataclass
class Client:
    # информация о клиенте
    client_id: UUID
    full_name: str
    age: int
    gender: Gender
    phone: str
    location: str
