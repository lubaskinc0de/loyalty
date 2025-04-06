import sqlalchemy as sa
from geoalchemy2.types import Geography

from loyalty.adapters.db.registry import mapper_registry
from loyalty.domain.entity.client import Client
from loyalty.domain.shared_types import Gender

metadata = mapper_registry.metadata

client_table = sa.Table(
    "client",
    metadata,
    sa.Column("client_id", sa.UUID(as_uuid=True), primary_key=True),
    sa.Column("full_name", sa.String(250), nullable=False),
    sa.Column("age", sa.Integer, nullable=False),
    sa.Column("location", Geography("POINT", srid=4326), nullable=False),
    sa.Column("gender", sa.Enum(Gender), nullable=False),
    sa.Column("phone", sa.String(50), nullable=False),
)

mapper_registry.map_imperatively(Client, client_table)
