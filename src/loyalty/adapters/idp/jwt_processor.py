from dataclasses import dataclass
from datetime import UTC, datetime

import jwt
from adaptix import Retort

from loyalty.adapters.idp.access_token import AccessToken

retort = Retort()
ALG = "HS256"


@dataclass(slots=True, frozen=True)
class AccessTokenProcessor:
    secret_key: str

    def encode(self, token: AccessToken) -> str:
        payload = retort.dump(token)
        return jwt.encode(
            {
                "iat": datetime.now(tz=UTC),
                "sub": payload,
            },
            self.secret_key,
            ALG,
        )

    def decode(self, content: str) -> AccessToken:
        payload = jwt.decode(content, self.secret_key, algorithms=[ALG])
        return retort.load(payload["sub"], AccessToken)
