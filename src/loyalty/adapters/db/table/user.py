import sqlalchemy as sa
from sqlalchemy.orm import relationship

from loyalty.adapters.auth.user import WebUser
from loyalty.adapters.db.registry import mapper_registry
from loyalty.domain.entity.business import Business
from loyalty.domain.entity.client import Client
from loyalty.domain.entity.user import User

metadata = mapper_registry.metadata


user_table = sa.Table(
    "users",
    metadata,
    sa.Column("user_id", sa.UUID(as_uuid=True), primary_key=True),
    sa.Column(
        "client_id",
        sa.UUID(as_uuid=True),
        sa.ForeignKey("client.client_id", ondelete="SET NULL"),
        nullable=True,
    ),
    sa.Column(
        "business_id",
        sa.UUID(as_uuid=True),
        sa.ForeignKey("business.business_id", ondelete="SET NULL"),
        nullable=True,
    ),
)

web_user_table = sa.Table(
    "web_user",
    metadata,
    sa.Column("web_user_id", sa.UUID(as_uuid=True), primary_key=True),
    sa.Column("user_id", sa.UUID(as_uuid=True), sa.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False),
    sa.Column("username", sa.String(250), nullable=False, unique=True, index=True),
    sa.Column("hashed_password", sa.Text, nullable=False),
)

mapper_registry.map_imperatively(
    User,
    user_table,
    properties={
        "business": relationship(Business, lazy="selectin"),
        "client": relationship(Client, lazy="selectin"),
    },
)

mapper_registry.map_imperatively(
    WebUser,
    web_user_table,
    properties={
        "user": relationship(User, lazy="selectin"),
    },
)
