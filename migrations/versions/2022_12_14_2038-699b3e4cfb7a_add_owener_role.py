"""add_owener_role

Revision ID: 699b3e4cfb7a
Revises: 6b30180c8b04
Create Date: 2022-12-14 20:38:28.766863

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import insert, delete

from app.namespace.persistence.models import Role, RightEnum

# revision identifiers, used by Alembic.
revision = '699b3e4cfb7a'
down_revision = '6b30180c8b04'
branch_labels = None
depends_on = None


def upgrade() -> None:
    connection = op.get_bind()
    stmt = insert(
        Role
    ).values(
        name='Владелец',
        slug='owner',
        rights=[RightEnum.VIEW, RightEnum.EDIT_ITEMS, RightEnum.EDIT_USERS, RightEnum.EDIT_NAMESPACE]
    )
    connection.execute(stmt)


def downgrade() -> None:
    connection = op.get_bind()
    stmt = delete(
        Role
    ).where(
        Role.slug == 'owner'
    )

    connection.execute(stmt)
