from dataclasses import dataclass
from uuid import UUID

from loyalty.application.common.idp import Role
from loyalty.domain.entity.business import Business
from loyalty.domain.entity.client import Client


@dataclass
class WebUser:
    # учетные данные пользователя по которым его можно аутентифицировать
    user_id: UUID
    username: str
    hashed_password: str
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


@dataclass
class TelegramUser:
    user_id: UUID
    telegram_id: int
