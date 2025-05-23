"""['constraints']

Revision ID: 0709f1a35a57
Revises: 156acf76eb1c
Create Date: 2025-05-07 16:55:30.704674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0709f1a35a57'
down_revision = '156acf76eb1c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('uq_membership', 'loyalty_membership', ['loyalty_id', 'client_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uq_membership', 'loyalty_membership', type_='unique')
    # ### end Alembic commands ###