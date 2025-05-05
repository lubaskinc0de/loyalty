from dataclasses import dataclass
from enum import Enum
from uuid import UUID

from loyalty.domain.entity.business import Business
from loyalty.domain.entity.client import Client


class Role(Enum):
    CLIENT = "client"
    BUSINESS = "business"


@dataclass
class User:
    user_id: UUID
    business: Business | None = None
    client: Client | None = None

    @property
    def available_roles(self) -> list[Role]:
        role_fields = ["business", "client"]
        role_map = {
            "client": Role.CLIENT,
            "business": Role.BUSINESS,
        }
        result = []

        for field in role_fields:
            if getattr(self, field, None) is not None:
                result.append(role_map[field])  # noqa: PERF401
        return result

    def is_one_of(self, *roles: Role) -> bool:
        available = self.available_roles
        matches = [x for x in roles if x in available]
        return bool(matches)

    def can_create_client(self) -> bool:
        return not self.is_one_of(Role.CLIENT)

    def can_create_business(self) -> bool:
        return not self.is_one_of(Role.BUSINESS)
