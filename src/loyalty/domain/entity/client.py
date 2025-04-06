from dataclasses import dataclass
from uuid import UUID

from loyalty.domain.shared_types import Gender


@dataclass(frozen=True, slots=True)
class Client:
    # информация о клиенте
    client_id: UUID
    full_name: str
    age: int
    city: str
    gender: Gender
    phone: str
