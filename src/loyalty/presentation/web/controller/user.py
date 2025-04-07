from uuid import uuid4

from pydantic import BaseModel, Field

from loyalty.adapters.hasher import Hasher
from loyalty.adapters.user import User
from loyalty.application.common.gateway.user_gateway import UserGateway


class UserCredentials(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=6, max_length=100)


def create_user(form: UserCredentials, hasher: Hasher, gateway: UserGateway) -> User:
    hashed_password = hasher.hash(form.password)
    user_id = uuid4()
    user = User(user_id, form.username, hashed_password)
    gateway.insert(user)

    return user
