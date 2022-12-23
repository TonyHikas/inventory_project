"""add_roles

Revision ID: f8e7e8106b57
Revises: b8184ebd2ae4
Create Date: 2022-12-23 10:21:03.254520

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import insert, delete

from app.namespace.persistence.models import Role, RightEnum

# revision identifiers, used by Alembic.
revision = 'f8e7e8106b57'
down_revision = 'b8184ebd2ae4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    connection = op.get_bind()
    stmt1 = insert(
        Role
    ).values(
        name='Редактор',
        slug='editor',
        rights=[RightEnum.VIEW, RightEnum.EDIT_ITEMS]
    )
    stmt2 = insert(
        Role
    ).values(
        name='Зритель',
        slug='viewer',
        rights=[RightEnum.VIEW]
    )

    connection.execute(stmt1)
    connection.execute(stmt2)


def downgrade() -> None:
    connection = op.get_bind()
    stmt1 = delete(
        Role
    ).where(
        Role.slug == 'editor'
    )
    stmt2 = delete(
        Role
    ).where(
        Role.slug == 'viewer'
    )

    connection.execute(stmt1)
    connection.execute(stmt2)
