"""empty message

Revision ID: 9ef4d3b5a1a5
Revises: 1ad46927e2a4
Create Date: 2023-12-17 00:21:40.789507

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ef4d3b5a1a5'
down_revision: Union[str, None] = '1ad46927e2a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('days',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('presence', sa.Boolean(), nullable=False),
    sa.Column('mark', sa.Float(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('module_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['module_id'], ['modules.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('days')
    # ### end Alembic commands ###