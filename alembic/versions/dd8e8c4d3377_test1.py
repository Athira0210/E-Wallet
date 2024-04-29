"""test1

Revision ID: dd8e8c4d3377
Revises: b3df8bc88889
Create Date: 2024-04-22 16:06:59.003955

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd8e8c4d3377'
down_revision: Union[str, None] = 'b3df8bc88889'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaction', sa.Column('sender_id', sa.Integer(), nullable=True))
    op.add_column('transaction', sa.Column('receiver_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'transaction', 'user', ['receiver_id'], ['id'])
    op.create_foreign_key(None, 'transaction', 'user', ['sender_id'], ['id'])
    op.create_unique_constraint(None, 'user', ['email'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_constraint(None, 'transaction', type_='foreignkey')
    op.drop_constraint(None, 'transaction', type_='foreignkey')
    op.drop_column('transaction', 'receiver_id')
    op.drop_column('transaction', 'sender_id')
    # ### end Alembic commands ###
