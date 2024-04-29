"""test

Revision ID: 0f5d24ca5153
Revises: 8a1964527306
Create Date: 2024-04-22 12:22:11.356416

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0f5d24ca5153'
down_revision: Union[str, None] = '8a1964527306'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_account', sa.Column('amount', sa.Integer(), nullable=True))
    op.alter_column('user_account', 'balance',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_account', 'balance',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    op.drop_column('user_account', 'amount')
    # ### end Alembic commands ###
