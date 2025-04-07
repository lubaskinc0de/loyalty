import sqlalchemy as sa
from sqlalchemy.orm import relationship

from loyalty.adapters.auth.user import WebUser
from loyalty.adapters.db.registry import mapper_registry
from loyalty.domain.entity.business import Business
from loyalty.domain.entity.client import Client

metadata = mapper_registry.metadata


user_table = sa.Table(
    "users",
    metadata,
    sa.Column("user_id", sa.UUID(as_uuid=True), primary_key=True),
    sa.Column("username", sa.String(250), nullable=False, unique=True, index=True),
    sa.Column("hashed_password", sa.Text, nullable=False),
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

mapper_registry.map_imperatively(
    WebUser,
    user_table,
    properties={
        "business": relationship(Business, lazy="selectin"),
        "client": relationship(Client, lazy="selectin"),
    },
)
