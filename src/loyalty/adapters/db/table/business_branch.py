import sqlalchemy as sa
from geoalchemy2.types import Geography
from sqlalchemy.orm import relationship

from loyalty.adapters.db.registry import mapper_registry
from loyalty.domain.entity.business_branch import BusinessBranch

metadata = mapper_registry.metadata

business_branch_table = sa.Table(
    "business_branch",
    metadata,
    sa.Column("business_branch_id", sa.UUID(as_uuid=True), primary_key=True),
    sa.Column(
        "business_id",
        sa.UUID(as_uuid=True),
        sa.ForeignKey("business.business_id", ondelete="CASCADE"),
        nullable=True,
    ),
    sa.Column("name", sa.String(250), nullable=False, unique=False),
    sa.Column("contact_phone", sa.String(50), nullable=True),
    sa.Column("location", Geography("POINT", srid=4326), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True)),
)

mapper_registry.map_imperatively(
    BusinessBranch,
    business_branch_table,
    properties={
        "business": relationship("Business", lazy="selectin"),
    },
)
