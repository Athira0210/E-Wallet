"""test1

Revision ID: cb8dd41d3be5
Revises: dd8e8c4d3377
Create Date: 2024-04-23 09:57:27.453574

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb8dd41d3be5'
down_revision: Union[str, None] = 'dd8e8c4d3377'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_account_description', table_name='user_account')
    op.drop_index('ix_user_account_id', table_name='user_account')
    op.drop_table('user_account')
    op.add_column('user', sa.Column('amount', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'amount')
    op.create_table('user_account',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('amount', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='user_account_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='user_account_pkey')
    )
    op.create_index('ix_user_account_id', 'user_account', ['id'], unique=False)
    op.create_index('ix_user_account_description', 'user_account', ['description'], unique=False)
    # ### end Alembic commands ###
