from dataclasses import dataclass
from uuid import UUID

import sqlalchemy as sa

from loyalty.adapters.db.registry import mapper_registry
from loyalty.domain.entity.user import User

metadata = mapper_registry.metadata


@dataclass
class ClientUser:
    client_id: UUID
    user_id: UUID


user_table = sa.Table(
    "users",
    metadata,
    sa.Column("user_id", sa.UUID(as_uuid=True), primary_key=True),
    sa.Column("username", sa.String(250), nullable=False, unique=True, index=True),
    sa.Column("hashed_password", sa.Text, nullable=False),
)

client_user_table = sa.Table(
    "client_user",
    metadata,
    sa.Column("user_id", sa.UUID(as_uuid=True), sa.ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True),
    sa.Column(
        "client_id",
        sa.UUID(as_uuid=True),
        sa.ForeignKey("client.client_id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

mapper_registry.map_imperatively(User, user_table)
mapper_registry.map_imperatively(ClientUser, client_user_table)
