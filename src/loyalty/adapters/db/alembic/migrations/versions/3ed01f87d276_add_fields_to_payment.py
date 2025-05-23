"""add_fields_to_payment

Revision ID: 3ed01f87d276
Revises: fa26c269fcd5
Create Date: 2025-05-13 17:22:30.446817

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ed01f87d276'
down_revision = 'fa26c269fcd5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payment', sa.Column('bonus_spent', sa.Numeric(precision=10, scale=2), nullable=False))
    op.add_column('payment', sa.Column('discount_sum', sa.Numeric(precision=10, scale=2), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('payment', 'discount_sum')
    op.drop_column('payment', 'bonus_spent')
    # ### end Alembic commands ###