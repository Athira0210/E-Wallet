"""test1

Revision ID: b3df8bc88889
Revises: 2493db2ef943
Create Date: 2024-04-22 16:06:08.547491

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3df8bc88889'
down_revision: Union[str, None] = '2493db2ef943'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaction', sa.Column('sender_id', sa.String(), nullable=True))
    op.add_column('transaction', sa.Column('receiver_id', sa.String(), nullable=True))
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
