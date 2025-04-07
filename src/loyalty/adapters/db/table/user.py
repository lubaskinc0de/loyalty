from dataclasses import dataclass
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from loyalty.adapters.db.registry import mapper_registry
from loyalty.adapters.user import WebUser
from loyalty.domain.entity.business import Business
from loyalty.domain.entity.client import Client

metadata = mapper_registry.metadata


@dataclass
class ClientUser:
    client_id: UUID
    user_id: UUID
    client: Client


@dataclass
class BusinessUser:
    business_id: UUID
    user_id: UUID
    business: Business


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

business_user_table = sa.Table(
    "business_user",
    metadata,
    sa.Column("user_id", sa.UUID(as_uuid=True), sa.ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True),
    sa.Column(
        "business_id",
        sa.UUID(as_uuid=True),
        sa.ForeignKey("business.business_id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

mapper_registry.map_imperatively(WebUser, user_table)
mapper_registry.map_imperatively(
    ClientUser,
    client_user_table,
    properties={"client": relationship(Client, lazy="selectin")},
)
mapper_registry.map_imperatively(
    BusinessUser,
    business_user_table,
    properties={"business": relationship(Business, lazy="selectin")},
)
