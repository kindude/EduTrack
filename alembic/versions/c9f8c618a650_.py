"""empty message

Revision ID: c9f8c618a650
Revises: 9ef4d3b5a1a5
Create Date: 2024-01-16 00:00:36.157279

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import MetaData, Table

# revision identifiers, used by Alembic.
revision: str = 'c9f8c618a650'
down_revision: Union[str, None] = '9ef4d3b5a1a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop foreign key constraints
    op.drop_constraint('actions_user_id_fkey', 'actions', type_='foreignkey')
    op.drop_constraint('days_user_id_fkey', 'days', type_='foreignkey')

    # Alter columns
    op.alter_column('actions', 'user_id', ondelete='CASCADE')
    op.alter_column('days', 'user_id', ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade() -> None:

    op.create_foreign_key('actions_user_id_fkey', 'actions', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('days_user_id_fkey', 'days', 'users', ['user_id'], ['id'], ondelete='CASCADE')

    # Alter columns
    op.alter_column('actions', 'user_id', ondelete='SET NULL')
    op.alter_column('days', 'user_id', ondelete='SET NULL')
    # ### end Alembic commands ###
