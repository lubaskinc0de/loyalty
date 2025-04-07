from uuid import uuid4

from pydantic import BaseModel, Field

from loyalty.adapters.common.user_gateway import WebUserGateway
from loyalty.adapters.hasher import Hasher
from loyalty.adapters.user import WebUser


class WebUserCredentials(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=6, max_length=100)


def create_user(form: WebUserCredentials, hasher: Hasher, gateway: WebUserGateway) -> WebUser:
    hashed_password = hasher.hash(form.password)
    user_id = uuid4()
    user = WebUser(user_id, form.username, hashed_password)
    gateway.insert(user)

    return user
