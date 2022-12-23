"""add_funciton

Revision ID: 493173b35ec8
Revises: a07367093c2e
Create Date: 2022-12-23 11:33:40.251694

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '493173b35ec8'
down_revision = 'a07367093c2e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        '''
        CREATE FUNCTION short_line (text) RETURNS text AS $$
        select (substring ($1 from length ($1) - 10 ) || '...')
        $$ LANGUAGE sql;
        '''
    )


def downgrade() -> None:
    op.execute(
        '''
        DROP FUNCTION short_line (text);
        '''
    )
