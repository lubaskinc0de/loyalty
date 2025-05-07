import sqlalchemy as sa
from sqlalchemy.orm import relationship

from loyalty.adapters.db.registry import mapper_registry
from loyalty.domain.entity.membership import LoyaltyMembership

metadata = mapper_registry.metadata

loyalty_membership_table = sa.Table(
    "loyalty_membership",
    metadata,
    sa.Column("membership_id", sa.UUID(as_uuid=True), primary_key=True),
    sa.Column(
        "loyalty_id",
        sa.UUID(as_uuid=True),
        sa.ForeignKey("loyalty.loyalty_id", ondelete="CASCADE"),
        nullable=False,
    ),
    sa.Column(
        "client_id",
        sa.UUID(as_uuid=True),
        sa.ForeignKey("client.client_id", ondelete="CASCADE"),
        nullable=False,
    ),
    sa.Column("created_at", sa.DateTime(timezone=True)),
)

mapper_registry.map_imperatively(
    LoyaltyMembership,
    loyalty_membership_table,
    properties={
        "loyalty": relationship("Loyalty", lazy="selectin"),
        "client": relationship("Client", lazy="selectin"),
    },
)
