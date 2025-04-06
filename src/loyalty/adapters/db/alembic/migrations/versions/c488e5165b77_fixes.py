"""['fixes']

Revision ID: c488e5165b77
Revises: 90a9f34dd454
Create Date: 2025-04-06 10:07:15.929089

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c488e5165b77'
down_revision = '90a9f34dd454'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('client_user',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('client_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['client.client_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'client_id')
    )
    op.add_column('client', sa.Column('phone', sa.String(length=50), nullable=False))
    op.drop_constraint('client_user_id_fkey', 'client', type_='foreignkey')
    op.drop_column('client', 'user_id')
    op.drop_index('ix_user_username', table_name='users')
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.create_index('ix_user_username', 'users', ['username'], unique=True)
    op.add_column('client', sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False))
    op.create_foreign_key('client_user_id_fkey', 'client', 'users', ['user_id'], ['user_id'])
    op.drop_column('client', 'phone')
    op.drop_table('client_user')
    # ### end Alembic commands ###