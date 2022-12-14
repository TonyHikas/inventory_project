from sqlalchemy import Column, String, Integer, ForeignKey

from framework.persistence.mixins import CommonMixin
from framework.persistence.models import Base


class Location(Base, CommonMixin):
    __tablename__ = 'location'

    name = Column(String(511), nullable=False)
    address = Column(String(511), nullable=False)
    description = Column(String(3000), nullable=False)
    namespace_id = Column(
        Integer,
        ForeignKey('namespace.id', ondelete='CASCADE'),
        nullable=False
    )
