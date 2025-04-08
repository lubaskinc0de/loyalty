from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

import jwt

ALG = "HS256"


@dataclass(slots=True, frozen=True)
class AccessTokenProcessor:
    secret_key: str

    def encode(self, user_id: UUID) -> str:
        return jwt.encode(
            {
                "iat": datetime.now(tz=UTC),
                "sub": str(user_id),
            },
            self.secret_key,
            ALG,
        )

    def verify(self, content: str) -> None:
        jwt.decode(
            content,
            self.secret_key,
            algorithms=[ALG],
            options={
                "verify_exp": False,
            },
        )
