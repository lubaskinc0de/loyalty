import sqlalchemy as sa

from loyalty.adapters.db.registry import mapper_registry
from loyalty.domain.entity.user import User

metadata = mapper_registry.metadata

user_table = sa.Table(
    "users",
    metadata,
    sa.Column("user_id", sa.UUID(as_uuid=True), primary_key=True),
    sa.Column("username", sa.String(250), nullable=False, unique=True, index=True),
    sa.Column("hashed_password", sa.Text, nullable=False),
)

mapper_registry.map_imperatively(User, user_table)
