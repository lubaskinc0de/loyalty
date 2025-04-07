from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID


@dataclass
class Business:
    # информация о бизнесе - предприятии которое использует программу лояльности
    business_id: UUID
    name: str
    contact_phone: str | None
    contact_email: str
    location: str
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))
