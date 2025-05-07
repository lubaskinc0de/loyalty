from dataclasses import dataclass
from uuid import UUID

from loyalty.domain.entity.business import Business
from loyalty.domain.entity.client import Client
from loyalty.domain.vo.role import Role


@dataclass
class User:
    user_id: UUID
    business: Business | None = None
    client: Client | None = None

    @property
    def available_roles(self) -> list[Role]:
        role_map = {
            "client": Role.CLIENT,
            "business": Role.BUSINESS,
        }
        result = []

        for attr_name, role in role_map.items():
            if getattr(self, attr_name, None) is not None:
                result.append(role)
        return result

    def is_one_of(self, *roles: Role) -> bool:
        available = self.available_roles
        matches = [x for x in roles if x in available]
        return bool(matches)

    def can_create_client(self) -> bool:
        return not self.is_one_of(Role.CLIENT)

    def can_create_business(self) -> bool:
        return not self.is_one_of(Role.BUSINESS)
