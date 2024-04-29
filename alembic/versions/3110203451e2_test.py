"""test

Revision ID: 3110203451e2
Revises: cadcde749130
Create Date: 2024-04-22 15:58:28.433325

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3110203451e2'
down_revision: Union[str, None] = 'cadcde749130'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('transaction', 'sender_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=True)
    op.alter_column('transaction', 'receiver_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=True)
    op.drop_constraint('transaction_sender_id_fkey', 'transaction', type_='foreignkey')
    op.drop_constraint('transaction_receiver_id_fkey', 'transaction', type_='foreignkey')
    op.create_foreign_key(None, 'transaction', 'user', ['receiver_id'], ['email'])
    op.create_foreign_key(None, 'transaction', 'user', ['sender_id'], ['email'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'transaction', type_='foreignkey')
    op.drop_constraint(None, 'transaction', type_='foreignkey')
    op.create_foreign_key('transaction_receiver_id_fkey', 'transaction', 'user', ['receiver_id'], ['id'])
    op.create_foreign_key('transaction_sender_id_fkey', 'transaction', 'user', ['sender_id'], ['id'])
    op.alter_column('transaction', 'receiver_id',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('transaction', 'sender_id',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    # ### end Alembic commands ###
