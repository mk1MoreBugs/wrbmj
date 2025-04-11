"""create notes table

Revision ID: 036ed709365c
Revises: d0a8746cd428
Create Date: 2025-04-02 23:06:29.184314

"""
from typing import Sequence, Union

import sqlmodel
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '036ed709365c'
down_revision: Union[str, None] = 'd0a8746cd428'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('notes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('last_update', sa.DateTime(), nullable=False),
    sa.Column('title_name', sqlmodel.AutoString(length=84), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('note_content', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('notes')
