"""['Added business_branch table + changed business table']

Revision ID: 6c26017c7da0
Revises: 3cab696ef77e
Create Date: 2025-04-11 19:24:05.467095

"""
from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geography

# revision identifiers, used by Alembic.
revision = '6c26017c7da0'
down_revision = '3cab696ef77e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_geospatial_table('business_branch',
    sa.Column('business_branch_id', sa.UUID(), nullable=False),
    sa.Column('business_id', sa.UUID(), nullable=True),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('address', sa.String(length=250), nullable=False),
    sa.Column('contact_phone', sa.String(length=50), nullable=True),
    sa.Column('contact_email', sa.String(length=250), nullable=False),
    sa.Column('location', Geography(geometry_type='POINT', srid=4326, spatial_index=False, from_text='ST_GeogFromText', name='geography', nullable=False), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['business_id'], ['business.business_id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('business_branch_id'),
    sa.UniqueConstraint('address'),
    sa.UniqueConstraint('name')
    )
    op.create_geospatial_index('idx_business_branch_location', 'business_branch', ['location'], unique=False, postgresql_using='gist', postgresql_ops={})
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_geospatial_index('idx_business_branch_location', table_name='business_branch', postgresql_using='gist', column_name='location')
    op.drop_geospatial_table('business_branch')
    # ### end Alembic commands ###