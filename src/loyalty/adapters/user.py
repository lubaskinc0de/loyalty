from dataclasses import dataclass
from uuid import UUID


@dataclass
class User:
    # учетные данные пользователя по которым его можно аутентифицировать
    user_id: UUID
    username: str
    hashed_password: str
