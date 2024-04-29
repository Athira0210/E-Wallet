"""test

Revision ID: 4f96425c8071
Revises: 0e830c78ac66
Create Date: 2024-04-19 16:17:25.487423

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f96425c8071'
down_revision: Union[str, None] = '0e830c78ac66'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_account',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('balance', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_account_description'), 'user_account', ['description'], unique=False)
    op.create_index(op.f('ix_user_account_id'), 'user_account', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_account_id'), table_name='user_account')
    op.drop_index(op.f('ix_user_account_description'), table_name='user_account')
    op.drop_table('user_account')
    # ### end Alembic commands ###
