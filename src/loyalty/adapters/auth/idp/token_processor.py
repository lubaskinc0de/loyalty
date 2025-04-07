from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

import jwt

from loyalty.adapters.auth.access_token import AccessToken

ALG = "HS256"


@dataclass(slots=True, frozen=True)
class AccessTokenProcessor:
    secret_key: str

    def encode(self, user_id: UUID) -> str:
        return jwt.encode(
            {
                "iat": datetime.now(tz=UTC),
                "sub": {
                    "user_id": str(user_id),
                },
            },
            self.secret_key,
            ALG,
        )

    def decode(self, content: str) -> AccessToken:
        payload = jwt.decode(content, self.secret_key, algorithms=[ALG])
        return AccessToken(user_id=UUID(payload["sub"]), token=content)
