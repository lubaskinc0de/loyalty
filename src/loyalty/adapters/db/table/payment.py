import sqlalchemy as sa

from loyalty.adapters.db.registry import mapper_registry
from loyalty.domain.entity.payment import Payment

metadata = mapper_registry.metadata

payment_table = sa.Table(
    "payment",
    metadata,
    sa.Column("payment_id", sa.UUID(as_uuid=True), primary_key=True),
    sa.Column(
        "client_id",
        sa.UUID(as_uuid=True),
        sa.ForeignKey("client.client_id", ondelete="SET NULL"),
        nullable=True,
    ),
    sa.Column(
        "loyalty_id",
        sa.UUID(as_uuid=True),
        sa.ForeignKey("loyalty.loyalty_id", ondelete="SET NULL"),
        nullable=True,
    ),
    sa.Column(
        "membership_id",
        sa.UUID(as_uuid=True),
        sa.ForeignKey("loyalty_membership.membership_id", ondelete="SET NULL"),
        nullable=True,
    ),
    sa.Column(
        "business_id",
        sa.UUID(as_uuid=True),
        sa.ForeignKey("business.business_id", ondelete="SET NULL"),
        nullable=True,
    ),
    sa.Column(
        "business_branch_id",
        sa.UUID(as_uuid=True),
        sa.ForeignKey("business_branch.business_branch_id", ondelete="SET NULL"),
        nullable=True,
    ),
    sa.Column("payment_sum", sa.Numeric(10, 2), nullable=False),
    sa.Column("service_income", sa.Numeric(10, 2), nullable=False),
    sa.Column("bonus_income", sa.Numeric(10, 2), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True)),
)

mapper_registry.map_imperatively(
    Payment,
    payment_table,
)
