"""['Changed', 'loyalty', 'table', 'money_per_bonus', 'field', 'type_']

Revision ID: d4a49e4c9de5
Revises: a6a23b9da163
Create Date: 2025-05-09 19:15:47.750806

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4a49e4c9de5'
down_revision = 'a6a23b9da163'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('loyalty', 'money_per_bonus',
               existing_type=sa.INTEGER(),
               type_=sa.Numeric(precision=10, scale=2),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('loyalty', 'money_per_bonus',
               existing_type=sa.Numeric(precision=10, scale=2),
               type_=sa.INTEGER(),
               existing_nullable=False)
    # ### end Alembic commands ###