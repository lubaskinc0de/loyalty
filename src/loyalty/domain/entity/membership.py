from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from loyalty.domain.entity.business import Business
from loyalty.domain.entity.client import Client
from loyalty.domain.entity.loyalty import Loyalty


@dataclass
class LoyaltyMembership:
    # Участие в программе лояльности
    membership_id: UUID
    loyalty: Loyalty
    client: Client
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))

    def can_edit(self, client: Client) -> bool:
        return self.client.client_id == client.client_id

    def can_read(self, client: Client) -> bool:
        return self.can_edit(client)

    def is_owner_client(self, client: Client) -> bool:
        return self.can_edit(client)

    def is_owner_business(self, business: Business) -> bool:
        return self.loyalty.business.business_id == business.business_id

