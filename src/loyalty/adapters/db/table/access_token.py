import sqlalchemy as sa

from loyalty.adapters.auth.access_token import AccessToken
from loyalty.adapters.db import mapper_registry

metadata = mapper_registry.metadata

access_token_table = sa.Table(
    "access_token",
    metadata,
    sa.Column("user_id", sa.UUID(as_uuid=True), sa.ForeignKey("users.user_id", ondelete="CASCADE")),
    sa.Column("token", sa.Text, nullable=False, unique=True),
)

mapper_registry.map_imperatively(AccessToken, access_token_table)
