"""test

Revision ID: 355a024e12aa
Revises: 76f447ca787d
Create Date: 2024-04-21 23:11:04.302468

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '355a024e12aa'
down_revision: Union[str, None] = '76f447ca787d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
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
    # ### end Alembic commands ###
