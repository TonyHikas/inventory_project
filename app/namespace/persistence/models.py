import enum

from sqlalchemy import Column, String, Integer, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY

from framework.persistence.mixins import CommonMixin
from framework.persistence.models import Base


class RightEnum(str, enum.Enum):
    VIEW = 'VIEW'
    EDIT_ITEMS = 'EDIT_ITEMS'
    EDIT_NAMESPACE = 'EDIT_NAMESPACE'
    EDIT_USERS = 'EDIT_USERS'


class Namespace(Base, CommonMixin):
    __tablename__ = 'namespace'

    name = Column(String(511), nullable=False)


class Role(Base, CommonMixin):
    __tablename__ = 'role'

    name = Column(
        String(255),
        nullable=False
    )

    slug = Column(
        String(50),
        nullable=False,
        unique=True
    )

    rights = Column(
        ARRAY(Enum(RightEnum))
    )


class UserNamespace(Base, CommonMixin):
    __tablename__ = 'user_namespace'

    user_id = Column(
        Integer,
        ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False
    )
    namespace_id = Column(
        Integer,
        ForeignKey('namespace.id', ondelete='CASCADE'),
        nullable=False
    )
    role_id = Column(
        Integer,
        ForeignKey('role.id', ondelete='CASCADE'),
        nullable=False
    )
    __table_args__ = (
        UniqueConstraint('user_id', 'namespace_id', 'role_id', name='user_namespace_role_constraint'),
    )
