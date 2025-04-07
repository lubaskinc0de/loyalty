import sqlalchemy as sa
from sqlalchemy.orm import relationship

from loyalty.adapters.auth.access_token import AccessToken
from loyalty.adapters.auth.user import WebUser
from loyalty.adapters.db import mapper_registry

metadata = mapper_registry.metadata

access_token_table = sa.Table(
    "access_token",
    metadata,
    sa.Column("user_id", sa.UUID(as_uuid=True), sa.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False),
    sa.Column("token", sa.Text, nullable=False, primary_key=True),
)

mapper_registry.map_imperatively(
    AccessToken,
    access_token_table,
    properties={"user": relationship(WebUser, lazy="selectin")},
)
