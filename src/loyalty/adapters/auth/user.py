from dataclasses import dataclass
from uuid import UUID


@dataclass
class WebUser:
    # учетные данные пользователя по которым его можно аутентифицировать
    user_id: UUID
    username: str
    hashed_password: str


@dataclass
class TelegramUser:
    user_id: UUID
    telegram_id: int
