from sqlalchemy import Column, ForeignKey, Table

from loyalty.adapters.db.registry import mapper_registry

metadata = mapper_registry.metadata

loyalties_to_branches_table = Table(
    "loyalties_to_branches_table",
    metadata,
    Column("loyalty_id", ForeignKey("loyalty.loyalty_id")),
    Column("business_branch_id", ForeignKey("business_branch.business_branch_id")),
)
