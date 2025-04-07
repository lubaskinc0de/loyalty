"""['timezone']

Revision ID: 609ea4dbf58f
Revises: 5493b7169389
Create Date: 2025-04-07 08:30:45.372210

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '609ea4dbf58f'
down_revision = '5493b7169389'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('client', sa.Column('created_at', sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('client', 'created_at')
    # ### end Alembic commands ###