from sqlalchemy import Column, String, Integer, ForeignKey

from framework.persistence.mixins import CommonMixin, IdMixin
from framework.persistence.models import Base


class Namespace(Base, CommonMixin):
    __tablename__ = 'namespace'

    name = Column(String, nullable=False)
    created_by = Column(
        Integer,
        ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False
    )

class Role(Base, IdMixin):
    __tablename__ = 'role'

    name = Column(String, nullable=False, unique=True)


class UserNamespace(Base, CommonMixin):
    __tablename__ = 'user_namespace'

    # todo make user and namespace id unique
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
