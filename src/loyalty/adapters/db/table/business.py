import sqlalchemy as sa
from sqlalchemy.orm import relationship

from loyalty.adapters.db.registry import mapper_registry
from loyalty.domain.entity.business import Business

metadata = mapper_registry.metadata

business_table = sa.Table(
    "business",
    metadata,
    sa.Column("business_id", sa.UUID(as_uuid=True), primary_key=True),
    sa.Column("name", sa.String(250), nullable=False, unique=True),
    sa.Column("contact_phone", sa.String(50), nullable=True),
    sa.Column("contact_email", sa.String(250), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True)),
)

mapper_registry.map_imperatively(
    Business,
    business_table,
    properties={"branches": relationship("BusinessBranch", back_populates="business", lazy="selectin", uselist=True)},
)
