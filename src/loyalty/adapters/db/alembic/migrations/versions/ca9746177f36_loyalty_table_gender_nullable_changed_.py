"""['loyalty table gender nullable changed to True']

Revision ID: ca9746177f36
Revises: cd493300587b
Create Date: 2025-04-29 20:26:03.782135

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ca9746177f36'
down_revision = 'cd493300587b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('loyalty', 'gender',
               existing_type=postgresql.ENUM('MALE', 'FEMALE', name='gender'),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('loyalty', 'gender',
               existing_type=postgresql.ENUM('MALE', 'FEMALE', name='gender'),
               nullable=False)
    # ### end Alembic commands ###