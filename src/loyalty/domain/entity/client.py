from dataclasses import dataclass, field
from datetime import UTC, datetime
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
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))
