import sqlalchemy as sa
from sqlalchemy.orm import relationship

from loyalty.adapters.db.registry import mapper_registry
from loyalty.domain.entity.loyalty import Loyalty
from loyalty.domain.shared_types import Gender

from .association_tables import loyalties_to_branches_table

metadata = mapper_registry.metadata

loyalty_table = sa.Table(
    "loyalty",
    metadata,
    sa.Column("loyalty_id", sa.UUID(as_uuid=True), primary_key=True),
    sa.Column(
        "business_id",
        sa.UUID(as_uuid=True),
        sa.ForeignKey("business.business_id", ondelete="CASCADE"),
        nullable=True,
    ),
    sa.Column("name", sa.String(100), nullable=False, unique=False),
    sa.Column("description", sa.String(950), nullable=False, unique=False),
    sa.Column("starts_at", sa.DateTime(timezone=True)),
    sa.Column("ends_at", sa.DateTime(timezone=True)),
    sa.Column("money_per_bonus", sa.Integer, nullable=False),
    sa.Column("min_age", sa.Integer, nullable=False),
    sa.Column("max_age", sa.Integer, nullable=False),
    sa.Column("is_active", sa.Boolean, nullable=False),
    sa.Column("gender", sa.Enum(Gender), nullable=True),
    sa.Column("created_at", sa.DateTime(timezone=True)),
)

mapper_registry.map_imperatively(
    Loyalty,
    loyalty_table,
    properties={
        "business": relationship("Business", lazy="selectin"),
        "business_branches": relationship(
            "BusinessBranch",
            lazy="selectin",
            secondary=loyalties_to_branches_table,
        ),
    },
)
