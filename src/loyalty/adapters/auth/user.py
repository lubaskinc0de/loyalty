from dataclasses import dataclass
from uuid import UUID

from loyalty.domain.entity.user import User


@dataclass
class WebUser:
    web_user_id: UUID
    username: str
    hashed_password: str
    user: User


@dataclass
class TelegramUser:
    user_id: UUID
    telegram_id: int
