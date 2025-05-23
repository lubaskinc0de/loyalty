"""['remove business location']

Revision ID: c6f37c863d6a
Revises: 962ae5860807
Create Date: 2025-04-08 16:09:45.702489

"""
from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geography

# revision identifiers, used by Alembic.
revision = 'c6f37c863d6a'
down_revision = '962ae5860807'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_geospatial_index('idx_business_location', table_name='business', postgresql_using='gist', column_name='location')
    op.drop_geospatial_column('business', 'location')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_geospatial_column('business', sa.Column('location', Geography(geometry_type='POINT', srid=4326, spatial_index=False, from_text='ST_GeogFromText', name='geography', nullable=False), autoincrement=False, nullable=False))
    op.create_geospatial_index('idx_business_location', 'business', ['location'], unique=False, postgresql_using='gist', postgresql_ops={})
    # ### end Alembic commands ###